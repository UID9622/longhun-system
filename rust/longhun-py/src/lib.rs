// DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-RUST-PYTHON-BINDINGS-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 协议: MulanPSL v2 (工程层)
// 模块: 龍魂Rust内核 → Python PyO3绑定
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

use lhcore::core::{SupervisionConfig, run_supervision, get_health};
use lhcore::memory::{query as memory_query, create_memory};
use lhcore::evolution::{
    TriggerReason, MeltdownFactory,
    GateRunner,
    check_data_blackhole, detect_veto_word, detect_forbidden_scenario,
    governance_self_check,
};

use pyo3::prelude::*;
use pyo3::types::PyDict;

// ═══════════════════════════════════════════════════════════════
// Python 模块入口
// ═══════════════════════════════════════════════════════════════

#[pymodule]
fn longhun_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("DNA", "#龍芯⚡️丙午·丙申·壬子·子时·䷕贲-RUST-CORE-v2.0-UID9622")?;
    m.add("VERSION", "2.0.0")?;
    m.add("AUTHOR", "诸葛鑫（UID9622）")?;

    // 核心
    m.add_class::<PySupervisionConfig>()?;
    m.add_function(wrap_pyfunction!(py_run_supervision, m)?)?;
    m.add_function(wrap_pyfunction!(py_get_health, m)?)?;

    // 记忆
    m.add_function(wrap_pyfunction!(py_query_memory, m)?)?;
    m.add_function(wrap_pyfunction!(py_create_memory, m)?)?;

    // 治理
    m.add_class::<PyMeltdownState>()?;
    m.add_function(wrap_pyfunction!(py_meltdown, m)?)?;
    m.add_function(wrap_pyfunction!(py_detect_veto_word, m)?)?;
    m.add_function(wrap_pyfunction!(py_detect_forbidden, m)?)?;
    m.add_function(wrap_pyfunction!(py_check_blackhole, m)?)?;
    m.add_function(wrap_pyfunction!(py_governance_check, m)?)?;
    m.add_function(wrap_pyfunction!(py_gate_check, m)?)?;

    Ok(())
}

// ═══════════════════════════════════════════════════════════════
// 核心
// ═══════════════════════════════════════════════════════════════

#[pyclass(name = "SupervisionConfig")]
#[derive(Clone)]
struct PySupervisionConfig {
    #[pyo3(get, set)]
    sensitivity: f64,
}

#[pymethods]
impl PySupervisionConfig {
    #[new]
    fn new(sensitivity: f64) -> Self {
        PySupervisionConfig { sensitivity }
    }
}

#[pyfunction]
fn py_run_supervision(config: Option<PySupervisionConfig>) -> PyResult<PyObject> {
    let cfg = SupervisionConfig {
        sensitivity: config.map(|c| c.sensitivity).unwrap_or(0.7),
        dna_verify: true,
        audit_enabled: true,
        max_deviation: 20.0,
    };
    let report = run_supervision(&cfg);
    Python::with_gil(|py| {
        let dict = PyDict::new(py);
        dict.set_item("score", report.score)?;
        dict.set_item("audit", format!("{:?}", report.audit))?;
        dict.set_item("dna_valid", report.dna_valid)?;
        dict.set_item("timestamp", report.timestamp)?;
        dict.set_item("recommendations", report.recommendations)?;
        Ok(dict.into())
    })
}

#[pyfunction]
fn py_get_health() -> PyResult<PyObject> {
    let h = get_health();
    Python::with_gil(|py| {
        let dict = PyDict::new(py);
        dict.set_item("status", h.status)?;
        dict.set_item("cpu_percent", h.cpu_percent)?;
        dict.set_item("memory_used_mb", h.memory_used_mb)?;
        dict.set_item("memory_total_mb", h.memory_total_mb)?;
        dict.set_item("uptime_seconds", h.uptime_seconds)?;
        dict.set_item("active_services", h.active_services)?;
        Ok(dict.into())
    })
}

// ═══════════════════════════════════════════════════════════════
// 记忆
// ═══════════════════════════════════════════════════════════════

#[pyfunction]
fn py_query_memory(query_str: &str) -> PyResult<Vec<PyObject>> {
    let results = memory_query(query_str);
    Python::with_gil(|py| {
        results.entries.iter().map(|e| {
            let dict = PyDict::new(py);
            dict.set_item("id", &e.id)?;
            dict.set_item("priority", format!("{:?}", e.priority))?;
            dict.set_item("content", &e.content)?;
            dict.set_item("dna", &e.dna)?;
            dict.set_item("tags", &e.tags)?;
            dict.set_item("created_at", &e.created_at)?;
            dict.set_item("frozen", e.frozen)?;
            Ok(dict.into())
        }).collect()
    })
}

#[pyfunction]
fn py_create_memory(content: &str, tags: Vec<String>) -> PyResult<PyObject> {
    let e = create_memory(content, tags);
    Python::with_gil(|py| {
        let dict = PyDict::new(py);
        dict.set_item("id", &e.id)?;
        dict.set_item("priority", format!("{:?}", e.priority))?;
        dict.set_item("content", &e.content)?;
        dict.set_item("dna", &e.dna)?;
        dict.set_item("tags", &e.tags)?;
        dict.set_item("created_at", &e.created_at)?;
        dict.set_item("frozen", e.frozen)?;
        Ok(dict.into())
    })
}

// ═══════════════════════════════════════════════════════════════
// 治理
// ═══════════════════════════════════════════════════════════════

#[pyclass(name = "MeltdownState")]
#[derive(Clone)]
struct PyMeltdownState {
    #[pyo3(get)]
    level: String,
    #[pyo3(get)]
    reason: String,
    #[pyo3(get)]
    detail: String,
    #[pyo3(get)]
    triggered: bool,
    #[pyo3(get)]
    tripped_by: String,
    #[pyo3(get)]
    recoverable: bool,
    #[pyo3(get)]
    recovery_condition: String,
    #[pyo3(get)]
    affected_scope: String,
    #[pyo3(get)]
    dna: String,
}

#[pyfunction]
fn py_meltdown(level: &str, reason: &str, detail: &str) -> PyResult<PyMeltdownState> {
    let ms = match level.to_lowercase().as_str() {
        "infinite" | "l0" => MeltdownFactory::infinite(
            TriggerReason::Custom(reason.to_string()), detail
        ),
        "data" | "l1" => MeltdownFactory::data(
            TriggerReason::Custom(reason.to_string()), detail
        ),
        "persona" | "l2" => MeltdownFactory::persona(
            TriggerReason::Custom(reason.to_string()), "unknown", detail
        ),
        "behavior" | "l3" => MeltdownFactory::behavior(
            TriggerReason::Custom(reason.to_string()), detail
        ),
        _ => return Err(pyo3::exceptions::PyValueError::new_err(
            format!("未知熔断级别: {}. 可选: infinite/l0, data/l1, persona/l2, behavior/l3", level)
        )),
    };
    Ok(PyMeltdownState {
        level: format!("{:?}", ms.level),
        reason: ms.reason.as_str().to_string(),
        detail: ms.detail,
        triggered: ms.triggered,
        tripped_by: ms.tripped_by,
        recoverable: ms.recoverable,
        recovery_condition: ms.recovery_condition,
        affected_scope: ms.affected_scope,
        dna: ms.dna,
    })
}

#[pyfunction]
fn py_detect_veto_word(content: &str) -> Option<(String, String)> {
    detect_veto_word(content).map(|(w, d)| (w.to_string(), d.to_string()))
}

#[pyfunction]
fn py_detect_forbidden(content: &str) -> Vec<String> {
    detect_forbidden_scenario(content)
}

#[pyfunction]
fn py_check_blackhole(content: &str) -> Option<(u8, String)> {
    check_data_blackhole(content)
}

#[pyfunction]
fn py_governance_check(content: &str) -> PyResult<PyObject> {
    let r = governance_self_check(content);
    Python::with_gil(|py| {
        let dict = PyDict::new(py);
        dict.set_item("audit_mark", &r.audit_mark)?;
        dict.set_item("veto_clean", r.veto_clean)?;
        dict.set_item("gate_clean", r.gate_clean)?;
        dict.set_item("blackhole_hits", &r.blackhole_hits)?;
        dict.set_item("recommendations", &r.recommendations)?;
        dict.set_item("timestamp", &r.timestamp)?;
        dict.set_item("dna", &r.dna)?;
        Ok(dict.into())
    })
}

#[pyfunction]
fn py_gate_check(content: &str) -> PyResult<PyObject> {
    let mut runner = GateRunner::new();
    let report = runner.run_all(content, "python-gate-check");
    Python::with_gil(|py| {
        let dict = PyDict::new(py);
        dict.set_item("total", report.total)?;
        dict.set_item("passed", report.passed)?;
        dict.set_item("failed", report.failed)?;
        dict.set_item("pending", report.pending)?;
        dict.set_item("is_clean", report.is_clean())?;
        dict.set_item("timestamp", &report.timestamp)?;
        Ok(dict.into())
    })
}
