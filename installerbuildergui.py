#!/usr/bin/env python3
"""
Installer Builder Frontend GUI

Wizard-like tool that generates installer scripts for Inno Setup or NSIS
based on user input, and optionally runs the compiler to create an installer.

This is a portfolio/demo app, not a full-featured installer authoring tool.
"""

import os
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox, scrolledtext


class InstallerBuilderGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Installer Builder Frontend")
        self.root.geometry("950x750")
        self.root.minsize(900, 700)

        # Basic app metadata
        self.app_name_var = tk.StringVar(value="MyApp")
        self.app_version_var = tk.StringVar(value="1.0.0")
        self.publisher_var = tk.StringVar(value="My Company")
        self.app_dir_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.main_exe_var = tk.StringVar()
        self.license_file_var = tk.StringVar()

        # Installer choices
        self.installer_type_var = tk.StringVar(value="inno")
        self.create_desktop_var = tk.BooleanVar(value=True)
        self.create_startmenu_var = tk.BooleanVar(value=True)

        # Paths to compilers (user can override)
        self.innosetup_compiler_var = tk.StringVar(
            value=r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
        )
        self.nsis_compiler_var = tk.StringVar(
            value=r"C:\Program Files (x86)\NSIS\makensis.exe"
        )

        self.status_var = tk.StringVar(value="Ready")

        self.create_widgets()

    # ---------------------------
    # UI
    # ---------------------------
    def create_widgets(self) -> None:
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            main_frame,
            text="Installer Builder Frontend",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))

        # App info
        info_frame = ttk.LabelFrame(main_frame, text="Application Info", padding="8")
        info_frame.grid(row=1, column=0, sticky=tk.EW, pady=4)
        info_frame.columnconfigure(1, weight=1)

        ttk.Label(info_frame, text="App Name:", width=16).grid(
            row=0, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(info_frame, textvariable=self.app_name_var).grid(
            row=0, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )

        ttk.Label(info_frame, text="Version:", width=16).grid(
            row=1, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(info_frame, textvariable=self.app_version_var).grid(
            row=1, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )

        ttk.Label(info_frame, text="Publisher:", width=16).grid(
            row=2, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(info_frame, textvariable=self.publisher_var).grid(
            row=2, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )

        ttk.Label(info_frame, text="App Directory:", width=16).grid(
            row=3, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(info_frame, textvariable=self.app_dir_var).grid(
            row=3, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )
        ttk.Button(
            info_frame, text="Browse...", command=self.browse_app_dir, width=10
        ).grid(row=3, column=2, sticky=tk.W, pady=3)

        ttk.Label(info_frame, text="Main EXE:", width=16).grid(
            row=4, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(info_frame, textvariable=self.main_exe_var).grid(
            row=4, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )
        ttk.Button(
            info_frame, text="Browse...", command=self.browse_main_exe, width=10
        ).grid(row=4, column=2, sticky=tk.W, pady=3)

        ttk.Label(info_frame, text="License File:", width=16).grid(
            row=5, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(info_frame, textvariable=self.license_file_var).grid(
            row=5, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )
        ttk.Button(
            info_frame, text="Browse...", command=self.browse_license, width=10
        ).grid(row=5, column=2, sticky=tk.W, pady=3)

        ttk.Label(info_frame, text="Output Dir:", width=16).grid(
            row=6, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(info_frame, textvariable=self.output_dir_var).grid(
            row=6, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )
        ttk.Button(
            info_frame, text="Browse...", command=self.browse_output_dir, width=10
        ).grid(row=6, column=2, sticky=tk.W, pady=3)

        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Installer Options", padding="8")
        options_frame.grid(row=2, column=0, sticky=tk.EW, pady=4)
        options_frame.columnconfigure(0, weight=1)

        ttk.Label(options_frame, text="Installer Type:").grid(
            row=0, column=0, sticky=tk.W, pady=3
        )

        type_frame = ttk.Frame(options_frame)
        type_frame.grid(row=0, column=1, sticky=tk.W, pady=3)

        ttk.Radiobutton(
            type_frame,
            text="Inno Setup",
            variable=self.installer_type_var,
            value="inno",
        ).pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(
            type_frame,
            text="NSIS",
            variable=self.installer_type_var,
            value="nsis",
        ).pack(side=tk.LEFT, padx=2)

        ttk.Checkbutton(
            options_frame,
            text="Create Desktop Shortcut",
            variable=self.create_desktop_var,
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Checkbutton(
            options_frame,
            text="Create Start Menu Shortcut",
            variable=self.create_startmenu_var,
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Compiler paths
        compiler_frame = ttk.LabelFrame(main_frame, text="Compiler Paths", padding="8")
        compiler_frame.grid(row=3, column=0, sticky=tk.EW, pady=4)
        compiler_frame.columnconfigure(1, weight=1)

        ttk.Label(compiler_frame, text="Inno Setup ISCC.exe:", width=20).grid(
            row=0, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(compiler_frame, textvariable=self.innosetup_compiler_var).grid(
            row=0, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )
        ttk.Button(
            compiler_frame,
            text="Browse...",
            command=self.browse_inno_compiler,
            width=10,
        ).grid(row=0, column=2, sticky=tk.W, pady=3)

        ttk.Label(compiler_frame, text="NSIS makensis.exe:", width=20).grid(
            row=1, column=0, sticky=tk.W, pady=3
        )
        ttk.Entry(compiler_frame, textvariable=self.nsis_compiler_var).grid(
            row=1, column=1, sticky=tk.EW, pady=3, padx=(0, 4)
        )
        ttk.Button(
            compiler_frame,
            text="Browse...",
            command=self.browse_nsis_compiler,
            width=10,
        ).grid(row=1, column=2, sticky=tk.W, pady=3)

        # Script preview / log
        preview_frame = ttk.LabelFrame(
            main_frame, text="Generated Script Preview / Log", padding="8"
        )
        preview_frame.grid(row=4, column=0, sticky=tk.NSEW, pady=4)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        self.output_text = scrolledtext.ScrolledText(
            preview_frame, height=14, wrap=tk.WORD, font=("Consolas", 9)
        )
        self.output_text.grid(row=0, column=0, sticky=tk.NSEW)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, sticky=tk.EW, pady=8)

        ttk.Button(
            button_frame,
            text="Generate Script Only",
            command=self.generate_script_only,
            width=22,
        ).pack(side=tk.LEFT, padx=4)

        ttk.Button(
            button_frame,
            text="Generate Script and Build Installer",
            command=self.generate_and_build,
            width=32,
        ).pack(side=tk.LEFT, padx=4)

        # Status bar
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, sticky=tk.EW, pady=(4, 0))

    # ---------------------------
    # Helpers
    # ---------------------------
    def log(self, msg: str) -> None:
        self.output_text.insert(tk.END, msg + "\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()

    def browse_app_dir(self) -> None:
        folder = filedialog.askdirectory(title="Select application directory")
        if folder:
            self.app_dir_var.set(folder)

    def browse_main_exe(self) -> None:
        filename = filedialog.askopenfilename(
            title="Select main executable",
            filetypes=[("Executables", "*.exe"), ("All files", "*.*")],
        )
        if filename:
            self.main_exe_var.set(filename)
            if not self.app_dir_var.get():
                self.app_dir_var.set(os.path.dirname(filename))

    def browse_license(self) -> None:
        filename = filedialog.askopenfilename(
            title="Select license text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if filename:
            self.license_file_var.set(filename)

    def browse_output_dir(self) -> None:
        folder = filedialog.askdirectory(title="Select output directory")
        if folder:
            self.output_dir_var.set(folder)

    def browse_inno_compiler(self) -> None:
        filename = filedialog.askopenfilename(
            title="Locate ISCC.exe (Inno Setup Compiler)",
            filetypes=[("Executable", "ISCC.exe"), ("All files", "*.*")],
        )
        if filename:
            self.innosetup_compiler_var.set(filename)

    def browse_nsis_compiler(self) -> None:
        filename = filedialog.askopenfilename(
            title="Locate makensis.exe (NSIS Compiler)",
            filetypes=[("Executable", "makensis.exe"), ("All files", "*.*")],
        )
        if filename:
            self.nsis_compiler_var.set(filename)

    # ---------------------------
    # Script generation
    # ---------------------------
    def _validate_basic(self) -> bool:
        if not self.app_name_var.get().strip():
            messagebox.showerror("Validation", "Please enter App Name.")
            return False
        if not self.app_version_var.get().strip():
            messagebox.showerror("Validation", "Please enter App Version.")
            return False
        if not self.app_dir_var.get().strip():
            messagebox.showerror("Validation", "Please select App Directory.")
            return False
        if not os.path.isdir(self.app_dir_var.get().strip()):
            messagebox.showerror(
                "Validation", "App Directory does not exist or is not a directory."
            )
            return False
        if not self.main_exe_var.get().strip():
            messagebox.showerror("Validation", "Please select Main EXE.")
            return False
        if not os.path.isfile(self.main_exe_var.get().strip()):
            messagebox.showerror("Validation", "Main EXE path is not a file.")
            return False
        if not self.output_dir_var.get().strip():
            messagebox.showerror("Validation", "Please select Output Directory.")
            return False
        if not os.path.isdir(self.output_dir_var.get().strip()):
            messagebox.showerror(
                "Validation", "Output Directory does not exist or is not a directory."
            )
            return False
        return True

    def generate_script_only(self) -> None:
        if not self._validate_basic():
            return
        self.output_text.delete("1.0", tk.END)
        installer_type = self.installer_type_var.get()
        if installer_type == "inno":
            script_content, script_path = self._generate_inno_script()
        else:
            script_content, script_path = self._generate_nsis_script()

        self.output_text.insert(tk.END, script_content)
        self.log(f"\nScript written to: {script_path}")
        self.status_var.set("Script generated.")

    def generate_and_build(self) -> None:
        if not self._validate_basic():
            return
        self.output_text.delete("1.0", tk.END)
        installer_type = self.installer_type_var.get()
        if installer_type == "inno":
            script_content, script_path = self._generate_inno_script()
            compiler = self.innosetup_compiler_var.get().strip()
            cmd = [compiler, script_path]
        else:
            script_content, script_path = self._generate_nsis_script()
            compiler = self.nsis_compiler_var.get().strip()
            cmd = [compiler, script_path]

        self.output_text.insert(tk.END, script_content)
        self.log(f"\nScript written to: {script_path}")

        if not compiler or not os.path.isfile(compiler):
            self.log("Compiler executable not found; skipping build.")
            messagebox.showwarning(
                "Build Installer",
                "Compiler executable not found.\n\n"
                "Script was generated, but installer was not built.",
            )
            self.status_var.set("Script generated; build skipped.")
            return

        self.log(f"\nRunning compiler: {' '.join(cmd)}")
        self.status_var.set("Building installer...")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
            )
            self.log("\n=== Compiler Output ===")
            self.log(result.stdout or "")
            self.log(result.stderr or "")
            if result.returncode == 0:
                self.status_var.set("Installer build succeeded.")
                messagebox.showinfo(
                    "Build Installer", "Installer build completed successfully."
                )
            else:
                self.status_var.set("Installer build failed.")
                messagebox.showerror(
                    "Build Installer",
                    "Installer build failed.\n\nSee compiler output in the log.",
                )
        except Exception as exc:
            self.log(f"\nERROR: Failed to run compiler:\n{exc}")
            self.status_var.set("Compiler error.")
            messagebox.showerror(
                "Build Installer", f"Failed to run compiler:\n\n{exc}"
            )

    def _generate_inno_script(self) -> tuple[str, str]:
        """Generate a simple Inno Setup script."""
        app_name = self.app_name_var.get().strip()
        app_version = self.app_version_var.get().strip()
        publisher = self.publisher_var.get().strip()
        app_dir = self.app_dir_var.get().strip()
        main_exe = self.main_exe_var.get().strip()
        license_file = self.license_file_var.get().strip()
        output_dir = self.output_dir_var.get().strip()

        main_exe_name = os.path.basename(main_exe)

        lines = [
            f'#define MyAppName "{app_name}"',
            f'#define MyAppVersion "{app_version}"',
            f'#define MyAppPublisher "{publisher}"',
            f'#define MyAppExeName "{main_exe_name}"',
            "",
            "[Setup]",
            'AppId={{' + app_name + "}",
            'AppName={#MyAppName}',
            'AppVersion={#MyAppVersion}',
            'AppPublisher={#MyAppPublisher}',
            'DefaultDirName={pf}\\{#MyAppName}',
            f"DefaultGroupName={app_name}",
            f'OutputDir={output_dir.replace("\\\\", "\\\\")}',
            'OutputBaseFilename={#MyAppName}-{#MyAppVersion}-Setup',
            "Compression=lzma",
            "SolidCompression=yes",
        ]

        if license_file:
            lines.append(f'LicenseFile={license_file.replace("\\\\", "\\\\")}')

        lines.extend(
            [
                "",
                "[Languages]",
                'Name: "english"; MessagesFile: "compiler:Default.isl"',
                "",
                "[Tasks]",
            ]
        )

        if self.create_desktop_var.get():
            lines.append(
                'Name: "desktopicon"; Description: "Create a &desktop icon"; '
                'GroupDescription: "Additional icons:"; Flags: unchecked'
            )

        lines.extend(
            [
                "",
                "[Files]",
                f'Source: "{app_dir}\\*"; DestDir: "{{app}}"; Flags: recursesubdirs ignoreversion',
                "",
                "[Icons]",
            ]
        )

        if self.create_startmenu_var.get():
            lines.append(
                'Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"'
            )

        if self.create_desktop_var.get():
            lines.append(
                'Name: "{commondesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; '
                'Tasks: desktopicon'
            )

        script_content = "\n".join(lines) + "\n"

        script_path = os.path.join(output_dir, f"{app_name}_inno.iss")
        Path(script_path).write_text(script_content, encoding="utf-8")
        return script_content, script_path

    def _generate_nsis_script(self) -> tuple[str, str]:
        """Generate a simple NSIS script."""
        app_name = self.app_name_var.get().strip()
        app_version = self.app_version_var.get().strip()
        publisher = self.publisher_var.get().strip()
        app_dir = self.app_dir_var.get().strip()
        main_exe = self.main_exe_var.get().strip()
        license_file = self.license_file_var.get().strip()
        output_dir = self.output_dir_var.get().strip()
        main_exe_name = os.path.basename(main_exe)

        install_dir_var = "$PROGRAMFILES64" if os.name == "nt" else "$PROGRAMFILES"

        lines = [
            f'Name "{app_name}"',
            f'OutFile "{os.path.join(output_dir, f"{app_name}-{app_version}-Setup.exe")}"',
            f'InstallDir "{install_dir_var}\\{app_name}"',
            "SetCompress auto",
            "SetCompressor /SOLID lzma",
            "",
            "RequestExecutionLevel admin",
            "",
            "Page directory",
            "Page instfiles",
        ]

        if license_file:
            lines.insert(6, f'LicenseData "{license_file}"')

        lines.extend(
            [
                "",
                "Section \"Install\"",
                f'  SetOutPath "$INSTDIR"',
                f'  File /r "{app_dir}\\*.*"',
            ]
        )

        if self.create_startmenu_var.get():
            lines.extend(
                [
                    f'  CreateDirectory "$SMPROGRAMS\\{app_name}"',
                    f'  CreateShortCut "$SMPROGRAMS\\{app_name}\\{app_name}.lnk" '
                    f'"$INSTDIR\\{main_exe_name}"',
                ]
            )

        if self.create_desktop_var.get():
            lines.append(
                f'  CreateShortCut "$DESKTOP\\{app_name}.lnk" "$INSTDIR\\{main_exe_name}"'
            )

        lines.extend(
            [
                "SectionEnd",
            ]
        )

        script_content = "\n".join(lines) + "\n"

        script_path = os.path.join(output_dir, f"{app_name}_nsis.nsi")
        Path(script_path).write_text(script_content, encoding="utf-8")
        return script_content, script_path


def main() -> None:
    root = tk.Tk()
    app = InstallerBuilderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

