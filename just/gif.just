# ── Spinning-logo gif ─────────────────────────────────────────

img := "assets/wallago.png"
frames := "assets/spin"
gif := "assets/wallago-spin.gif"
script := "scripts/spin.py"
fps := "30"
width := "250"

# Render the rotating frames with headless Blender
[group('gif')]
render:
    mkdir -p {{ frames }}
    nix run nixpkgs#blender -- --background --python {{ script }}

# Stitch the rendered frames into a high-quality (opaque) gif via gifski
[group('gif')]
gif:
    nix run nixpkgs#gifski -- --fps {{ fps }} --width {{ width }} \
        -o {{ gif }} {{ frames }}/frame_*.png

# Transparent gif variant via ffmpeg palette (needs a transparent-bg source)
[group('gif')]
gif-transparent:
    nix run nixpkgs#ffmpeg -- -y \
        -framerate {{ fps }} -i {{ frames }}/frame_%04d.png \
        -vf "split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=128" \
        {{ gif }}

# Render frames then build the gif in one go
[group('gif')]
all: render gif

# Remove generated frames and the gif
[group('gif')]
clean:
    rm -rf {{ frames }} {{ gif }}
