import { Component, type ErrorInfo, type ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('[ErrorBoundary]', error, info.componentStack)
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback
      return (
        <div className="flex min-h-[50vh] flex-col items-center justify-center gap-6 px-6 text-center">
          <span
            className="select-none font-serif text-[80px] font-black leading-none text-gold/10"
            aria-hidden="true"
          >
            ䷀
          </span>
          <h2 className="font-serif text-2xl font-bold text-paper">页面暂时无法显示</h2>
          <p className="max-w-[400px] text-[15px] leading-relaxed text-paper-dim">
            {this.state.error?.message || '组件渲染时发生未知错误，请稍后重试。'}
          </p>
          <button
            onClick={this.handleRetry}
            className="rounded-lg border border-gold/30 bg-ink px-6 py-2.5 text-[15px] text-gold transition-all hover:border-gold/60 hover:bg-gold/5"
          >
            重新加载
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
