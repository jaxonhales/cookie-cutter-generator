"""
main.py
Cookie Cutter Generator — converts a sharpie line drawing photo to a printable STL.

Usage:
    python main.py drawing.png output.stl [options]
    python main.py --gui          (launches drag-and-drop window)

Options:
    --height FLOAT          Wall height in mm (default: 50)
    --wall FLOAT            Wall thickness in mm (default: 2.0)
    --flange-width FLOAT    Inner base flange width in mm (default: 5.0)
    --flange-height FLOAT   Base flange height in mm (default: 2.5)
    --dpi FLOAT             DPI of input image for scale (default: 96)
    --size FLOAT            Force output size: longest dimension in mm (default: None)
    --smooth FLOAT          Spline smoothing factor (default: auto)
    --gui                   Launch graphical interface
"""

import argparse
import sys
import os


def run_pipeline(
    image_path: str,
    output_path: str,
    wall_height: float = 50.0,
    wall_thickness: float = 2.0,
    flange_width: float = 5.0,
    flange_height: float = 2.5,
    dpi: float = 96.0,
    force_size_mm: float = None,
    smoothing: float = None,
):
    """Full pipeline: image → STL."""
    from image_to_spline import image_to_spline
    from spline_to_stl import pixel_pts_to_mm, build_cookie_cutter_v2, save_stl
    import numpy as np

    print("=" * 50)
    print("  Cookie Cutter Generator")
    print("=" * 50)

    # Step 1: Image → spline points in pixel space
    spline_px, is_closed = image_to_spline(image_path, smoothing=smoothing)

    # Step 2: Convert pixels → mm
    pixels_per_mm = dpi / 25.4  # 1 inch = 25.4mm

    if force_size_mm is not None:
        # Override DPI-based scale: fit longest axis to force_size_mm
        extent = max(
            spline_px[:, 0].max() - spline_px[:, 0].min(),
            spline_px[:, 1].max() - spline_px[:, 1].min(),
        )
        pixels_per_mm = extent / force_size_mm
        print(f"  Scaling to fit {force_size_mm}mm (auto DPI: {pixels_per_mm:.2f} px/mm)")

    spline_mm = pixel_pts_to_mm(spline_px, pixels_per_mm)

    extent_x = spline_mm[:, 0].max() - spline_mm[:, 0].min()
    extent_y = spline_mm[:, 1].max() - spline_mm[:, 1].min()
    print(f"\n  Output dimensions: {extent_x:.1f} x {extent_y:.1f} mm")
    print(f"  Wall height:       {wall_height} mm")
    print(f"  Wall thickness:    {wall_thickness} mm")
    print(f"  Base flange:       {flange_width} mm wide × {flange_height} mm tall")
    print()

    # Step 3: Build 3D cookie cutter
    print("Building 3D geometry...")
    cutter = build_cookie_cutter_v2(
        spline_mm,
        is_closed=is_closed,
        wall_height=wall_height,
        wall_thickness=wall_thickness,
        base_flange_width=flange_width,
        base_flange_height=flange_height,
    )

    # Step 4: Export STL
    save_stl(cutter, output_path)

    print()
    print(f"✓ Cookie cutter saved to: {output_path}")
    print("  Ready to slice and print!")


def launch_gui():
    """Simple Tkinter drag-and-drop GUI."""
    import tkinter as tk
    from tkinter import filedialog, ttk, messagebox
    import threading

    root = tk.Tk()
    root.title("Cookie Cutter Generator")
    root.geometry("480x420")
    root.resizable(False, False)

    # ── State ──────────────────────────────────────────────────────────────
    image_path_var = tk.StringVar(value="No image selected")
    status_var = tk.StringVar(value="Select a drawing to get started.")

    # ── Layout ─────────────────────────────────────────────────────────────
    tk.Label(root, text="🍪 Cookie Cutter Generator", font=("Helvetica", 16, "bold")).pack(pady=12)

    # Image picker
    frame_img = tk.Frame(root, bd=2, relief=tk.GROOVE)
    frame_img.pack(fill=tk.X, padx=20, pady=4)
    tk.Label(frame_img, text="Drawing image:").pack(side=tk.LEFT, padx=6)
    tk.Label(frame_img, textvariable=image_path_var, fg="gray", width=28, anchor="w").pack(side=tk.LEFT)
    def pick_image():
        p = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if p:
            image_path_var.set(os.path.basename(p))
            image_path_var._full = p
    tk.Button(frame_img, text="Browse", command=pick_image).pack(side=tk.RIGHT, padx=6, pady=4)
    image_path_var._full = None

    # Parameters
    params = {}
    param_defs = [
        ("Wall height (mm)", "wall_height", "50"),
        ("Wall thickness (mm)", "wall_thickness", "2.0"),
        ("Base flange width (mm)", "flange_width", "5.0"),
        ("Base flange height (mm)", "flange_height", "2.5"),
        ("Force longest side to (mm, optional)", "force_size", ""),
        ("Image DPI (if known)", "dpi", "96"),
    ]
    frame_params = tk.LabelFrame(root, text="Parameters", padx=10, pady=6)
    frame_params.pack(fill=tk.X, padx=20, pady=8)
    for label, key, default in param_defs:
        row = tk.Frame(frame_params)
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text=label, width=30, anchor="w").pack(side=tk.LEFT)
        var = tk.StringVar(value=default)
        tk.Entry(row, textvariable=var, width=10).pack(side=tk.RIGHT)
        params[key] = var

    # Status
    tk.Label(root, textvariable=status_var, fg="blue", wraplength=440).pack(pady=4)
    progress = ttk.Progressbar(root, mode="indeterminate")
    progress.pack(fill=tk.X, padx=20)

    # Generate button
    def generate():
        img = getattr(image_path_var, "_full", None)
        if not img:
            messagebox.showerror("Error", "Please select an image first.")
            return

        out = filedialog.asksaveasfilename(
            defaultextension=".stl",
            filetypes=[("STL files", "*.stl")],
            initialfile="cookie_cutter.stl",
        )
        if not out:
            return

        def run():
            progress.start()
            status_var.set("Processing... this may take 30-60 seconds.")
            root.update()
            try:
                force_size = params["force_size"].get().strip()
                run_pipeline(
                    image_path=img,
                    output_path=out,
                    wall_height=float(params["wall_height"].get()),
                    wall_thickness=float(params["wall_thickness"].get()),
                    flange_width=float(params["flange_width"].get()),
                    flange_height=float(params["flange_height"].get()),
                    dpi=float(params["dpi"].get()),
                    force_size_mm=float(force_size) if force_size else None,
                )
                status_var.set(f"✓ Done! Saved to {os.path.basename(out)}")
            except Exception as e:
                status_var.set(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                progress.stop()

        threading.Thread(target=run, daemon=True).start()

    tk.Button(root, text="Generate STL", command=generate,
              bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
              height=2).pack(fill=tk.X, padx=20, pady=8)

    root.mainloop()


def cli():
    parser = argparse.ArgumentParser(description="Convert a sharpie drawing to a cookie cutter STL.")
    parser.add_argument("image", nargs="?", help="Input image path")
    parser.add_argument("output", nargs="?", help="Output STL path")
    parser.add_argument("--height", type=float, default=50.0, help="Wall height in mm")
    parser.add_argument("--wall", type=float, default=2.0, help="Wall thickness in mm")
    parser.add_argument("--flange-width", type=float, default=5.0, dest="flange_width")
    parser.add_argument("--flange-height", type=float, default=2.5, dest="flange_height")
    parser.add_argument("--dpi", type=float, default=96.0)
    parser.add_argument("--size", type=float, default=None, help="Force longest dimension to this many mm")
    parser.add_argument("--smooth", type=float, default=None)
    parser.add_argument("--gui", action="store_true", help="Launch GUI")
    args = parser.parse_args()

    if args.gui:
        launch_gui()
        return

    if not args.image or not args.output:
        parser.print_help()
        sys.exit(1)

    run_pipeline(
        image_path=args.image,
        output_path=args.output,
        wall_height=args.height,
        wall_thickness=args.wall,
        flange_width=args.flange_width,
        flange_height=args.flange_height,
        dpi=args.dpi,
        force_size_mm=args.size,
        smoothing=args.smooth,
    )


if __name__ == "__main__":
    cli()
