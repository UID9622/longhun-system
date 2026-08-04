#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·大有-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""Command line interface for Longhun WeChat Public Account integration."""

import argparse
import json
import sys
from pathlib import Path

from config import get_settings
from core import ArticleManager, MediaManager, WeChatClient
from services import ImageService, PersonaService, VoiceService


def cmd_config(args):
    """Show current configuration status."""
    settings = get_settings()
    status = settings.validate_wechat()
    print("=== 龍魂公众号集成配置 ===")
    print(f"公众号 AppID: {status['appid'] or '未设置'}")
    print(f"AppSecret: {'已设置' if settings.WECHAT_APPSECRET else '未设置'}")
    print(f"Kimi API Key: {'已设置' if settings.KIMI_API_KEY else '未设置'}")
    print(f"DeepSeek API Key: {'已设置' if settings.DEEPSEEK_API_KEY else '未设置'}")
    print(f"OpenAI API Key: {'已设置' if settings.OPENAI_API_KEY else '未设置'}")
    print(f"龍魂系统根目录: {settings.LONGHUN_SYSTEM_ROOT}")
    print(f"Web UI 端口: {settings.WEB_PORT}")
    if not status["ok"]:
        print("\n⚠️ 配置不完整：")
        for err in status["errors"]:
            print(f"  - {err}")
        print("\n请设置环境变量或编辑 .env 文件")
    else:
        print("\n✅ 配置完整，可以尝试获取 access_token")


def cmd_token(args):
    """Get or clear access token."""
    client = WeChatClient()
    if args.clear:
        client.clear_token_cache()
        print("✅ Access token 缓存已清除")
        return

    try:
        token = client.get_access_token(force_refresh=args.refresh)
        print(f"✅ Access token: {token[:16]}...")
        print(f"   缓存文件: {client.token_file}")
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        sys.exit(1)


def cmd_article_publish(args):
    """Publish an article."""
    manager = ArticleManager()

    if args.file:
        content = manager.read_file_content(args.file)
    elif args.content:
        content = args.content
    else:
        print("❌ 请提供 --file 或 --content")
        sys.exit(1)

    digest = args.digest or content[:100].replace("\n", "")
    cover_path = args.cover

    try:
        result = manager.create_draft(
            title=args.title,
            content=content,
            author=args.author,
            digest=digest,
            cover_image_path=cover_path,
            source_url=args.source_url,
        )
        print(f"✅ 草稿创建成功")
        print(f"   Media ID: {result['media_id']}")
        print(f"   标题: {args.title}")

        if not args.draft:
            pub_result = manager.publish(result["media_id"])
            print(f"✅ 发布任务提交成功")
            print(f"   Publish ID: {pub_result.get('publish_id')}")
            print(f"   Message Data ID: {pub_result.get('msg_data_id')}")

        dna = manager.generate_dna("DRAFT" if args.draft else "PUBLISH")
        print(f"   {dna}")

    except Exception as e:
        print(f"❌ 操作失败: {e}")
        sys.exit(1)


def cmd_article_list(args):
    """List draft articles."""
    manager = ArticleManager()
    try:
        result = manager.list_drafts(offset=args.offset, count=args.count)
        print(f"=== 草稿列表（共 {result.get('total_count', 0)} 篇）===")
        for item in result.get("item", []):
            media_id = item.get("media_id")
            content = item.get("content", {})
            news_item = content.get("news_item", [{}])[0]
            print(f"\nMedia ID: {media_id}")
            print(f"  标题: {news_item.get('title', 'N/A')}")
            print(f"  作者: {news_item.get('author', 'N/A')}")
            print(f"  更新时间: {item.get('update_time', 'N/A')}")
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        sys.exit(1)


def cmd_article_delete(args):
    """Delete a draft."""
    manager = ArticleManager()
    try:
        manager.delete_draft(args.media_id)
        print(f"✅ 草稿 {args.media_id} 已删除")
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        sys.exit(1)


def cmd_image_generate(args):
    """Generate an image."""
    service = ImageService()
    try:
        path = service.generate(
            prompt=args.prompt,
            output_path=args.output,
            width=args.width,
            height=args.height,
            style=args.style,
        )
        print(f"✅ 图片生成成功: {path}")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)


def cmd_voice_generate(args):
    """Generate a voice file."""
    service = VoiceService()
    try:
        path = service.generate(
            text=args.text,
            output_path=args.output,
            style=args.style,
            use_soul=args.soul,
        )
        print(f"✅ 语音生成成功: {path}")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)


def cmd_persona_list(args):
    """List personas."""
    service = PersonaService()
    personas = service.list_personas()
    print("=== 龍魂人格列表 ===")
    for p in personas:
        print(f"\n{p['icon']} {p['name']} ({p['id']})")
        print(f"   角色: {p['role']}")
        print(f"   描述: {p['description']}")


def cmd_persona_run(args):
    """Run a task with a persona."""
    service = PersonaService()
    try:
        result = service.route_task(args.task, persona_id=args.persona)
        print(f"=== {result['icon']} {result['name']} 输出 ===")
        if result.get("content"):
            print(result["content"])
        else:
            print("⚠️ " + result.get("note", "未生成内容"))
            print("\n提示词：")
            print(result.get("prompt", ""))
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        sys.exit(1)


def cmd_media_upload(args):
    """Upload media material."""
    media = MediaManager()
    try:
        result = media.upload_material(
            args.file,
            material_type=args.type,
            title=args.title,
            introduction=args.introduction,
        )
        print(f"✅ 素材上传成功")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="longhun-wechat",
        description="龍魂微信公众号智能内容中枢 CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # config
    subparsers.add_parser("config", help="查看配置状态")

    # token
    token_parser = subparsers.add_parser("token", help="获取/清除 access token")
    token_parser.add_argument("--refresh", action="store_true", help="强制刷新")
    token_parser.add_argument("--clear", action="store_true", help="清除缓存")

    # article
    article_parser = subparsers.add_parser("article", help="文章管理")
    article_sub = article_parser.add_subparsers(dest="article_cmd")

    publish_parser = article_sub.add_parser("publish", help="发布文章")
    publish_parser.add_argument("--title", required=True, help="文章标题")
    publish_parser.add_argument("--file", help="从文件读取内容")
    publish_parser.add_argument("--content", help="直接提供内容")
    publish_parser.add_argument("--author", help="作者")
    publish_parser.add_argument("--digest", help="摘要")
    publish_parser.add_argument("--cover", help="封面图片路径")
    publish_parser.add_argument("--source-url", help="原文链接")
    publish_parser.add_argument("--draft", action="store_true", help="仅创建草稿，不发布")

    list_parser = article_sub.add_parser("list", help="列出草稿")
    list_parser.add_argument("--offset", type=int, default=0)
    list_parser.add_argument("--count", type=int, default=20)

    delete_parser = article_sub.add_parser("delete", help="删除草稿")
    delete_parser.add_argument("media_id", help="草稿 Media ID")

    # image
    image_parser = subparsers.add_parser("image", help="AI 配图")
    image_sub = image_parser.add_subparsers(dest="image_cmd")
    img_gen = image_sub.add_parser("generate", help="生成配图")
    img_gen.add_argument("--prompt", required=True, help="图片描述")
    img_gen.add_argument("--output", help="输出路径")
    img_gen.add_argument("--width", type=int, default=900)
    img_gen.add_argument("--height", type=int, default=500)
    img_gen.add_argument(
        "--style",
        default="chinese_ink",
        choices=["chinese_ink", "modern", "minimal"],
        help="图片风格",
    )

    # voice
    voice_parser = subparsers.add_parser("voice", help="AI 语音")
    voice_sub = voice_parser.add_subparsers(dest="voice_cmd")
    voice_gen = voice_sub.add_parser("generate", help="生成语音")
    voice_gen.add_argument("--text", required=True, help="要朗读的文字")
    voice_gen.add_argument("--output", help="输出路径")
    voice_gen.add_argument(
        "--style",
        default="educator",
        choices=["storyteller", "educator", "passionate", "calm"],
        help="语音风格",
    )
    voice_gen.add_argument("--soul", action="store_true", help="使用 Soul 情感语音")

    # persona
    persona_parser = subparsers.add_parser("persona", help="人格管理")
    persona_sub = persona_parser.add_subparsers(dest="persona_cmd")
    persona_sub.add_parser("list", help="列出人格")
    run_parser = persona_sub.add_parser("run", help="运行人格任务")
    run_parser.add_argument("--persona", help="指定人格 ID")
    run_parser.add_argument("--task", required=True, help="任务描述")

    # media
    media_parser = subparsers.add_parser("media", help="素材管理")
    media_parser.add_argument("--file", required=True, help="文件路径")
    media_parser.add_argument(
        "--type",
        required=True,
        choices=["image", "voice", "video", "thumb"],
        help="素材类型",
    )
    media_parser.add_argument("--title", help="视频标题")
    media_parser.add_argument("--introduction", help="视频简介")

    args = parser.parse_args()

    if args.command == "config":
        cmd_config(args)
    elif args.command == "token":
        cmd_token(args)
    elif args.command == "article":
        if args.article_cmd == "publish":
            cmd_article_publish(args)
        elif args.article_cmd == "list":
            cmd_article_list(args)
        elif args.article_cmd == "delete":
            cmd_article_delete(args)
        else:
            article_parser.print_help()
    elif args.command == "image":
        if args.image_cmd == "generate":
            cmd_image_generate(args)
        else:
            image_parser.print_help()
    elif args.command == "voice":
        if args.voice_cmd == "generate":
            cmd_voice_generate(args)
        else:
            voice_parser.print_help()
    elif args.command == "persona":
        if args.persona_cmd == "list":
            cmd_persona_list(args)
        elif args.persona_cmd == "run":
            cmd_persona_run(args)
        else:
            persona_parser.print_help()
    elif args.command == "media":
        cmd_media_upload(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
