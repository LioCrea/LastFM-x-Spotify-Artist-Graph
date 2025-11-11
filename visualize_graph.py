from typing import Dict
from pyvis.network import Network

def visualize_track_graph(graph: Dict, output_html: str = "track_graph.html"):
    net = Network(height="800px", width="100%", bgcolor="#111", font_color="white")

    # Go to https://pyvis.readthedocs.io/en/latest/ to get all the details
    net.set_options("""
    {
      "nodes": {
        "shape": "dot",
        "size": 10,
        "font": { "color": "white" },
        "borderWidth": 2
      },
      "edges": {
        "color": { "color": "#555", "highlight": "#ffffff" },
        "width": 1,
        "smooth": false
      },
      "interaction": {
        "hover": true,
        "multiselect": false,
        "dragNodes": true
      },
      "physics": {
        "enabled": true,
        "stabilization": {
          "enabled": true,
          "iterations": 400
        },
        "forceAtlas2Based": {
          "gravitationalConstant": -120,
          "centralGravity": 0.01,
          "springLength": 250,
          "springConstant": 0.01,
          "avoidOverlap": 0.5
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)

    index = {}

    # nodes <> tracks
    for t in graph["tracks"]:
        track_id = t["id"]
        index[(t["name"], t["artist_name"])] = track_id
        net.add_node(
            track_id,
            label=t["name"],
            title=f"{t['name']} ({t['artist_name']})<br/>" + ", ".join(t.get("artist_genres", [])),
            group=t["artist_name"],
        )

    # edges <> links
    for e in graph["edges"]:
        key1 = (e["track1"], e["artist1"])
        key2 = (e["track2"], e["artist2"])
        if key1 not in index or key2 not in index:
            continue
        net.add_edge(
            index[key1],
            index[key2],
            title=", ".join(e.get("shared_genres", [])),
        )

    net.write_html(output_html)

    artists = sorted({t["artist_name"] for t in graph["tracks"]})

    artist_colors = {}
    for node in net.nodes:
        grp = node.get("group")
        color = node.get("color")
        if grp and color and grp not in artist_colors:
            artist_colors[grp] = color

    legend_items = []
    for artist in artists:
        col = artist_colors.get(artist, "#fff")
        legend_items.append(f'<div style="margin-bottom:4px;"><span style="display:inline-block;width:10px;height:10px;background:{col};border-radius:2px;margin-right:6px;"></span>{artist}</div>')
    legend_html = "\n".join(legend_items)

    draggable_block = f"""
<div id="legend" style="
    position: fixed;
    top: 20px;
    left: 20px;
    background: rgba(0,0,0,0.75);
    backdrop-filter: blur(4px);
    color: white;
    padding: 10px 14px;
    border-radius: 10px;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 13px;
    max-height: 300px;
    overflow-y: auto;
    z-index: 10000;
    cursor: move;
">
  <div style="font-weight:600;margin-bottom:6px;">Artists</div>
  {legend_html}
</div>

<script>
(function() {{
  const el = document.getElementById('legend');
  let isDown = false;
  let offsetX = 0;
  let offsetY = 0;

  el.addEventListener('mousedown', function(e) {{
    isDown = true;
    offsetX = e.clientX - el.offsetLeft;
    offsetY = e.clientY - el.offsetTop;
  }});

  document.addEventListener('mouseup', function() {{
    isDown = false;
  }});

  document.addEventListener('mousemove', function(e) {{
    if (!isDown) return;
    el.style.left = (e.clientX - offsetX) + 'px';
    el.style.top = (e.clientY - offsetY) + 'px';
  }});
}})();
</script>
"""
    with open(output_html, "a", encoding="utf-8") as f:
        f.write(draggable_block)

    print(f"Graph + draggable legend written to {output_html}")
