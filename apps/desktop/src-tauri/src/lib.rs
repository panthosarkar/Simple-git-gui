use std::process::{Child, Command};
use std::sync::Mutex;

use tauri::Manager;

struct BackendProcess(Mutex<Option<Child>>);

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_opener::init())
        .manage(BackendProcess(Mutex::new(None)))
        .setup(|app| {
            let project_root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../..")
                .canonicalize()
                .expect("Failed to resolve project root");

            let python = project_root.join(".venv/bin/python");
            let backend_script = project_root.join("backend/run_backend.py");

            let child = Command::new(python)
                .arg(backend_script)
                .current_dir(&project_root)
                .spawn()
                .expect("Failed to start Python backend");

            let state = app.state::<BackendProcess>();
            let mut guard = state
                .0
                .lock()
                .expect("Failed to lock backend process");

            *guard = Some(child);

            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::Destroyed = event {
                let state = window.state::<BackendProcess>();

                {
                    let mut guard = state
                        .0
                        .lock()
                        .expect("Failed to lock backend process");

                    if let Some(mut child) = guard.take() {
                        let _ = child.kill();
                        let _ = child.wait();
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}