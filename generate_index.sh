#!/bin/bash

BASE="/Volumes/External-SSD/blkpvnthr.github.io/assets/images"

# DGF
mkdir -p "$BASE/dgf"
cat > "$BASE/dgf/index.json" <<'JSON'
[
  { "src": "dgf-2.png", "title": "Dgf 2", "description": "Image: Dgf 2." },
  { "src": "dgf-3.png", "title": "Dgf 3", "description": "Image: Dgf 3." },
  { "src": "dgf-4.png", "title": "Dgf 4", "description": "Image: Dgf 4." },
  { "src": "dgf-5.png", "title": "Dgf 5", "description": "Image: Dgf 5." },
  { "src": "dgf-6.png", "title": "Dgf 6", "description": "Image: Dgf 6." },
  { "src": "dgf-7.png", "title": "Dgf 7", "description": "Image: Dgf 7." },
  { "src": "dgf-8.png", "title": "Dgf 8", "description": "Image: Dgf 8." },
  { "src": "dgf-9.png", "title": "Dgf 9", "description": "Image: Dgf 9." },
  { "src": "dgf-10.png", "title": "Dgf 10", "description": "Image: Dgf 10." },
  { "src": "dgf-11.png", "title": "Dgf 11", "description": "Image: Dgf 11." },
  { "src": "dgf-acronyms.png", "title": "Dgf Acronyms", "description": "Image: Dgf Acronyms." },
  { "src": "dgf-collaborator.png", "title": "Dgf Collaborator", "description": "Image: Dgf Collaborator." },
  { "src": "dgf-events.png", "title": "Dgf Events", "description": "Image: Dgf Events." },
  { "src": "DGF-external-map.png", "title": "DGF External Map", "description": "Image: DGF External Map." },
  { "src": "DGF-external.png", "title": "DGF External", "description": "Image: DGF External." },
  { "src": "dgf-images.png", "title": "Dgf Images", "description": "Image: Dgf Images." },
  { "src": "dgf-meetings.png", "title": "Dgf Meetings", "description": "Image: Dgf Meetings." },
  { "src": "dgf-news.png", "title": "Dgf News", "description": "Image: Dgf News." },
  { "src": "dgf-outreach.png", "title": "Dgf Outreach", "description": "Image: Dgf Outreach." },
  { "src": "dgf-swag.png", "title": "Dgf Swag", "description": "Image: Dgf Swag." },
  { "src": "dgf-videos.png", "title": "Dgf Videos", "description": "Image: Dgf Videos." },
  { "src": "dgf.png", "title": "Dgf Main", "description": "Image: Dgf Main." }
]
JSON

# Ezie Images
mkdir -p "$BASE/ezie-images"
cat > "$BASE/ezie-images/index.json" <<'JSON'
[
  { "src": "ezie.png", "title": "Ezie", "description": "Image: Ezie." },
  { "src": "ezie-3.png", "title": "Ezie 3", "description": "Image: Ezie 3." }
]
JSON

# Ice Giants
mkdir -p "$BASE/ice-giants"
cat > "$BASE/ice-giants/index.json" <<'JSON'
[
  { "src": "admin/ice-giants.png", "title": "Ice Giants Hero Layout", "description": "Image: Ice Giants Hero Layout." },
  { "src": "admin/ice-giants-2.png", "title": "Ice Giants Data Page", "description": "Image: Ice Giants Data Page." },
  { "src": "ps-images/updated-uranus-new.png", "title": "Updated Uranus (Concept Art)", "description": "Image: Updated Uranus (Concept Art)." }
]
JSON

# LOGIC
mkdir -p "$BASE/LOGIC"
cat > "$BASE/LOGIC/index.json" <<'JSON'
[
  { "src": "LOGIC/logic-manage-clock-2.png", "title": "Logic Manage Clock", "description": "Image: Logic Manage Clock." },
  { "src": "LOGIC/logic-faqs.png", "title": "Logic FAQs", "description": "Image: Logic FAQs." }
]
JSON

# Parker Kit
mkdir -p "$BASE/parker-kit"
cat > "$BASE/parker-kit/index.json" <<'JSON'
[
  { "src": "parker-kit.png", "title": "Parker Kit", "description": "Image: Parker Kit." }
]
JSON

# TIMED
mkdir -p "$BASE/TIMED"
cat > "$BASE/TIMED/index.json" <<'JSON'
[
  { "src": "timed-1.png", "title": "Timed 1", "description": "Image: Timed 1." },
  { "src": "timed-2.jpg", "title": "Timed 2", "description": "Image: Timed 2." }
]
JSON

# LAC
mkdir -p "$BASE/LAC"
cat > "$BASE/LAC/index.json" <<'JSON'
[
  { "src": "LAC.png", "title": "LAC", "description": "Image: LAC." },
  { "src": "LAC-2.png", "title": "LAC 2", "description": "Image: LAC 2." },
  { "src": "LAC-3.png", "title": "LAC 3", "description": "Image: LAC 3." }
]
JSON

echo "All index.json files generated under $BASE"
