# Cookie Cutter Generator — Setup Guide

---

## Files You Need

Download all of these from the chat before starting:

| File | What it does |
|------|-------------|
| `main.py` | The main program — handles the UI |
| `image_to_spline.py` | Reads your drawing and extracts the shape |
| `spline_to_stl.py` | Converts the shape into a 3D cookie cutter |
| `requirements.txt` | List of libraries the program needs |
| `build.sh` | Build script for Mac/Linux |
| `build.bat` | Build script for Windows |
| `build.yml` | Tells GitHub how to compile the program |

---

## Part 1 — Get the Files Ready on Your Mac

1. Create a folder on your Desktop called `cookie_cutter`

2. Put all the downloaded files inside it. The `.github/workflows/` folders you will need
to create manually. Your final folder should look exactly like this:

```
cookie_cutter/
├── .github/
│   └── workflows/
│       └── build.yml
├── main.py
├── image_to_spline.py
├── spline_to_stl.py
├── requirements.txt
├── build.sh
└── build.bat
```

> **How to create the `.github/workflows/` folders on Mac:**
> Open Terminal, and run:
> `mkdir -p ~/Desktop/cookie_cutter/.github/workflows`
> Then move `build.yml` into that `workflows` folder.

---

## Part 2 — Create a GitHub Account and Repo

3. Go to **https://github.com** and create a free account

4. Click **+** in the top right → **New repository**

5. Name it `cookie-cutter-generator`, set it to **Public**, click **Create repository**

6. On the repo page click **"uploading an existing file"**, drag your entire
`cookie_cutter` folder in, click **Commit changes**

---

## Part 3 — Let GitHub Build It

7. Click the **Actions** tab at the top of your repo — you'll see the build start automatically

8. Wait **10–15 minutes** for both the Windows and Mac jobs to show a green ✓

9. Click the completed run → scroll to **Artifacts** at the bottom → download both:
   - `CookieCutterGenerator-Windows` → the `.exe` file
   - `CookieCutterGenerator-Mac` → the Mac binary

---

## Part 4 — Send It to Someone

10. **Mac users:** Send them `CookieCutterGenerator`
    - First time: they right-click it → **Open** (Mac security thing)
    - After that: double-click works normally

11. **Windows users:** Send them `CookieCutterGenerator.exe`
    - If they see a blue warning screen, tell them to click **"More info" → "Run anyway"**
    - This is a false alarm, not a real virus warning

---

## Part 5 — Making Changes in the Future

12. Edit any of the `.py` files on your computer
13. Go back to GitHub and upload the changed files
14. GitHub automatically rebuilds both executables — go back to Step 7 to download the new versions

---

## How to Use the Program (for your end users)

1. Draw a shape on white paper with a black Sharpie
2. Take a photo or scan it
3. Open `CookieCutterGenerator`
4. Click **Browse** and select your photo
5. Set the size you want (e.g. `100` for a 100mm wide cutter)
6. Click **Generate STL**
7. Open the STL in your slicer (Cura, PrusaSlicer, etc.) and print!
