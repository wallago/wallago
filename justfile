# wallago spinning-logo gif pipeline
# run from the project root: `just` to list recipes

img := "assets/wallago.png"
frames := "assets/spin"
gif := "assets/wallago-spin.gif"
script := "scripts/spin.py"
fps := "30"
width := "250"

# list available recipes
default:
    @just --list

# render the rotating frames with headless Blender
render:
    mkdir -p {{ frames }}
    nix run nixpkgs#blender -- --background --python {{ script }}

# stitch the rendered frames into a high-quality (opaque) gif via gifski
gif:
    nix run nixpkgs#gifski -- --fps {{ fps }} --width {{ width }} \
        -o {{ gif }} {{ frames }}/frame_*.png

# transparent gif variant via ffmpeg palette (needs a transparent-bg source)
gif-transparent:
    nix run nixpkgs#ffmpeg -- -y \
        -framerate {{ fps }} -i {{ frames }}/frame_%04d.png \
        -vf "split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=128" \
        {{ gif }}

# render frames then build the gif in one go
all: render gif

# remove generated frames and the gif
clean:
    rm -rf {{ frames }} {{ gif }}
