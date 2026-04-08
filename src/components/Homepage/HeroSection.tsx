import React, {useEffect, useRef, useState, type ReactNode} from 'react';

export default function HeroSection(): ReactNode {
  const [svgContent, setSvgContent] = useState<string>('');
  const svgRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch('/images/home/hero-illustration.svg')
      .then(res => res.text())
      .then(text => setSvgContent(text))
      .catch(() => {});
  }, []);

  // Set up animations and interactivity after SVG loads
  useEffect(() => {
    if (!svgContent || !svgRef.current) return;
    const wrapper = svgRef.current.closest('.hero-illustration-wrapper');
    if (!wrapper) return;
    const svg = wrapper.querySelector('svg');
    if (!svg) return;

    // Restore all path/rect/circle fills that Docusaurus global CSS overrides.
    // The global rules force fill: none or fill: var(--svg-logo-color) on SVG paths,
    // which breaks the hero illustration's multi-colored content.
    svg.querySelectorAll('path, rect, circle, ellipse, polygon, polyline, line').forEach(el => {
      const fillAttr = el.getAttribute('fill');
      if (fillAttr) {
        (el as SVGElement).style.setProperty('fill', fillAttr, 'important');
      } else if (!el.getAttribute('stroke')) {
        (el as SVGElement).style.setProperty('fill', 'inherit', 'important');
      } else {
        (el as SVGElement).style.setProperty('fill', 'none', 'important');
      }
    });

    // Add Taylor Otwell avatar inside the blue circle node
    const blueCircle = svg.querySelector('circle[fill="#2563eb"]');
    if (blueCircle) {
      const ns = 'http://www.w3.org/2000/svg';
      const xlinkNs = 'http://www.w3.org/1999/xlink';
      const defs = svg.querySelector('defs') || svg.insertBefore(document.createElementNS(ns, 'defs'), svg.firstChild);

      // Create image element in defs
      const img = document.createElementNS(ns, 'image');
      img.setAttribute('id', 'hero-avatar-img');
      img.setAttribute('width', '512');
      img.setAttribute('height', '512');
      img.setAttribute('preserveAspectRatio', 'none');
      img.setAttributeNS(xlinkNs, 'href', '/images/home/taylor-otwell.avif');
      defs.appendChild(img);

      // Create pattern that uses the image
      const pattern = document.createElementNS(ns, 'pattern');
      pattern.setAttribute('id', 'hero-avatar-pattern');
      pattern.setAttribute('width', '1');
      pattern.setAttribute('height', '1');
      pattern.setAttribute('patternContentUnits', 'objectBoundingBox');
      const use = document.createElementNS(ns, 'use');
      use.setAttributeNS(xlinkNs, 'href', '#hero-avatar-img');
      use.setAttribute('transform', 'scale(.00195) rotate(-45) translate(-258 104)');
      use.classList.add('grayscale');
      pattern.appendChild(use);
      defs.appendChild(pattern);

      // Apply pattern fill to blue circle
      blueCircle.setAttribute('fill', 'url(#hero-avatar-pattern)');
      (blueCircle as SVGElement).style.setProperty('fill', 'url(#hero-avatar-pattern)', 'important');
    }

    // Fix "Cloud" text on the blue floor: gray #737373 is invisible on blue background.
    // The static SVG has "Cloud" in gray, but it should be white like the original site.
    // Note: children indices match the hero-illustration.svg structure (grid, base, building).
    const building = svg.children[1]?.children[2];
    if (building) {
      for (let i = 0; i < building.children.length; i++) {
        const floor = building.children[i];
        if (floor.getAttribute('style') === '--index: 0;') {
          floor.querySelectorAll('path[fill="#737373"]').forEach(p => {
            (p as SVGElement).style.setProperty('fill', '#fff', 'important');
          });
          break;
        }
      }
    }


    // Apply animation-delay to float groups
    const floatEls = svg.querySelectorAll('[class*="animate-float"]');
    floatEls.forEach(el => {
      (el as SVGElement).style.animationDelay = '400ms';
    });

    // Allow pointer events on hover rects inside the SVG
    const hoverRects = svg.querySelectorAll('[class*="pointer-events"]');
    hoverRects.forEach(rect => {
      (rect as SVGElement).style.pointerEvents = 'all';
    });

    // Enable pointer events on the icon area parent groups
    const iconGroups = svg.querySelectorAll('.cursor-pointer');
    iconGroups.forEach(el => {
      (el as SVGElement).style.pointerEvents = 'all';
    });

    // Icon cycling animation on building floors that have multiple icons.
    // Each icon slot has multiple SVGs; only one is visible at a time.
    // Visibility is controlled via opacity-0/blur-sm CSS classes.
    const buildingFloors = svg.children[1]?.children[2];
    if (buildingFloors) {
      // Map cell index to icon slot (only cells with multiple icons get a slot)
      const iconSlots: {icons: Element[]; current: number}[] = [];
      const cellToSlot: Record<number, number> = {};
      let cellIdx = 0;
      for (let i = 0; i < buildingFloors.children.length; i++) {
        const floor = buildingFloors.children[i];
        if (floor.tagName === 'defs') continue;
        const floorSvgs = floor.querySelectorAll('svg');
        if (floorSvgs.length > 1) {
          const icons = Array.from(floorSvgs).map(s => s.parentElement!);
          let current = icons.findIndex(p => !(p.getAttribute('class') || '').includes('opacity-0'));
          if (current === -1) current = 0;
          cellToSlot[cellIdx] = iconSlots.length;
          iconSlots.push({icons, current});
        }
        cellIdx++;
      }

      // Find the two moving highlight shapes on the icon grid.
      // They are g elements with transition-transform class inside the SVG.
      const allTT = svg.querySelectorAll('.transition-transform');
      const movingShapes = Array.from(allTT).filter(
        el => el.tagName === 'g' && el.parentElement?.tagName === 'g'
      );
      // Grid cell spacing in isometric coordinates
      const dx = 39.8485;
      const dy = -23.005;
      // 7 cells split into two zones: shape 0 → cells 3-6 (right), shape 1 → cells 0-2 (left)
      const shapeZones = [[3, 4, 5, 6], [0, 1, 2]];
      const shapePositions = [3, 0]; // initial cell positions
      const shapeZoneIdx = [0, 0]; // current index within each zone for sequential movement

      const moveShapeToCell = (shapeIdx: number, cell: number) => {
        if (shapeIdx >= movingShapes.length || !movingShapes[shapeIdx]) return;
        shapePositions[shapeIdx] = cell;
        const offsetX = (cell - 2) * dx;
        const offsetY = (cell - 2) * dy;
        (movingShapes[shapeIdx] as SVGElement).style.transform = `translate(${offsetX.toFixed(4)}px, ${offsetY.toFixed(4)}px)`;
      };

      // Set initial positions
      moveShapeToCell(0, shapePositions[0]);
      moveShapeToCell(1, shapePositions[1]);

      // Track which zones are paused by click
      const shapePaused = [false, false];

      // Add click handlers to icon cells using cursor-pointer groups
      const cursorGroups = svg.querySelectorAll('.cursor-pointer');
      cursorGroups.forEach((group, cellIdx) => {
        (group as SVGElement).style.pointerEvents = 'all';
        (group as SVGElement).style.cursor = 'pointer';
        // Enable pointer events on all ancestors up to svg
        let ancestor: Element | null = group.parentElement;
        while (ancestor && ancestor !== svg) {
          (ancestor as SVGElement).style.pointerEvents = 'all';
          ancestor = ancestor.parentElement;
        }
        group.addEventListener('click', () => {
          const zoneIdx = shapeZones.findIndex(zone => zone.includes(cellIdx));
          if (zoneIdx !== -1) {
            moveShapeToCell(zoneIdx, cellIdx);
            const newZonePos = shapeZones[zoneIdx].indexOf(cellIdx);
            shapeZoneIdx[zoneIdx] = newZonePos;
            // Sync building top to match clicked tile
            syncBuildingTop(zoneIdx, newZonePos);
          }
          // Pause both shapes on any click
          shapePaused[0] = true;
          shapePaused[1] = true;
        });
      });

      // Show a specific icon index in a slot, hiding all others via inline style
      const showSlotIcon = (slot: {icons: Element[]; current: number}, idx: number) => {
        const safeIdx = idx % slot.icons.length;
        slot.icons.forEach((icon, j) => {
          (icon as SVGElement).style.opacity = j === safeIdx ? '1' : '0';
          (icon as SVGElement).style.filter = j === safeIdx ? 'none' : 'blur(4px)';
          (icon as SVGElement).style.transition = 'opacity 300ms ease-out, filter 300ms ease-out';
        });
        slot.current = safeIdx;
      };

      // Find building top icon boxes via direct DOM paths
      // Cell 4 (floorChildIndex 8) → [8][2][2][0] has 4 child g elements (building top right)
      // Cell 6 (floorChildIndex 12) → [12][2][2][0] has 3 child g elements (building top left)
      const buildingTopSlots: {icons: Element[]; current: number; bgRects: Element[]}[] = [];
      const makeTopSlot = (floorIdx: number): {icons: Element[]; current: number; bgRects: Element[]} | null => {
        const floor = buildingFloors.children[floorIdx];
        if (!floor) return null;
        const group = floor.children[2]?.children[2]?.children[0];
        if (!group) return null;
        const icons = Array.from(group.children).filter(c => c.tagName === 'g');
        if (icons.length <= 1) return null;
        let current = icons.findIndex(g => !(g.getAttribute('class') || '').includes('opacity-0'));
        if (current === -1) current = 0;
        // Find transition-[fill] rects for background color
        const bgRects = Array.from(floor.querySelectorAll('rect')).filter(r =>
          (r.getAttribute('class') || '').includes('transition-[fill]')
        );
        return { icons, current, bgRects };
      };
      const rightTopSlot = makeTopSlot(8);   // 4 icons, syncs with right zone shape 0
      const leftTopSlot = makeTopSlot(12);   // 3 icons, syncs with left zone shape 1
      if (rightTopSlot) buildingTopSlots.push(rightTopSlot); // slot 0 = right (4 icons)
      if (leftTopSlot) buildingTopSlots.push(leftTopSlot);   // slot 1 = left (3 icons)

      // Background colors per icon index for each slot
      const bgColors: string[][] = [
        ['#4E243D', '#B2EDD3', '#087EA4', '#FE640B'], // right: Inertia, Vue, React, Svelte
        ['#222', '#1a73e8', '#D97757'],                 // left: Livewire, Chrome, Rust
      ];

      // Icons that need white fill on building top: [slotIdx][iconIdx]
      const whiteIcons: Record<string, boolean> = {
        '0-2': true, // right slot, icon 2 (React)
        '1-1': true, // left slot, icon 1 (Chrome)
        '1-2': true, // left slot, icon 2 (Rust)
      };

      // Sync building top box to shape zone index (icon + background)
      // shape 0 (right zone, cells 3-6) → buildingTopSlots[0] (4 icons)
      // shape 1 (left zone, cells 0-2) → buildingTopSlots[1] (3 icons)
      const syncBuildingTop = (shapeIdx: number, zoneIdx: number) => {
        const slotIdx = shapeIdx === 0 ? 0 : 1;
        if (slotIdx >= buildingTopSlots.length) return;
        const slot = buildingTopSlots[slotIdx];
        showSlotIcon(slot, zoneIdx);
        // Update background color
        const color = bgColors[slotIdx]?.[zoneIdx % (bgColors[slotIdx]?.length || 1)];
        if (color && slot.bgRects.length > 0) {
          slot.bgRects.forEach(rect => {
            (rect as SVGElement).style.fill = color;
          });
        }
        // Apply white fill to specific icons
        const safeIdx = zoneIdx % slot.icons.length;
        const needsWhite = whiteIcons[`${slotIdx}-${safeIdx}`];
        const iconEl = slot.icons[safeIdx] as SVGElement;
        if (iconEl) {
          const paths = iconEl.querySelectorAll('path, circle, ellipse, rect, polygon');
          paths.forEach(p => {
            if (needsWhite) {
              (p as SVGElement).dataset.origFill = (p as SVGElement).dataset.origFill || p.getAttribute('fill') || '';
              p.setAttribute('fill', 'white');
              (p as SVGElement).style.cssText += 'fill: white !important;';
            } else if ((p as SVGElement).dataset.origFill !== undefined) {
              p.setAttribute('fill', (p as SVGElement).dataset.origFill);
              (p as SVGElement).style.cssText = (p as SVGElement).style.cssText.replace(/fill:\s*white\s*!important;?/g, '');
            }
          });
        }
      };

      // Initial sync of building top icons to match shape starting positions
      syncBuildingTop(0, shapeZoneIdx[0]);
      syncBuildingTop(1, shapeZoneIdx[1]);

      if (iconSlots.length > 0) {
        const intervalId = setInterval(() => {
          // Skip everything if both shapes are paused
          if (shapePaused[0] && shapePaused[1]) return;

          // Move highlight shapes and sync building top
          movingShapes.forEach((_, i) => {
            if (i >= shapeZones.length || shapePaused[i]) return;
            const zone = shapeZones[i];
            shapeZoneIdx[i] = (shapeZoneIdx[i] + 1) % zone.length;
            const newCell = zone[shapeZoneIdx[i]];
            moveShapeToCell(i, newCell);
            syncBuildingTop(i, shapeZoneIdx[i]);
          });
        }, 2000);

        return () => clearInterval(intervalId);
      }
    }
  }, [svgContent]);

  return (
    <header className="hero-header">
      <div className="container" style={{position: 'relative'}}>
        {/* child 0: background grid pattern */}
        <div className="hero-grid-bg">
          <svg className="hero-grid-svg" width="100%" height="100%">
            <defs>
              <pattern id="hero-grid" x="-1" y="-1" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="transparent" stroke="currentColor" strokeWidth="1" />
              </pattern>
            </defs>
            <rect fill="url(#hero-grid)" width="100%" height="100%" />
          </svg>
        </div>

        {/* child 1: hero text section */}
        <section className="hero-text-section">
          <div className="hero-text-inner">
            <h1 className="hero-h1">The clean stack for{' '}<span className="hero-h1-br" />Artisans and agents.</h1>
            <p className="hero-subtitle">
              Laravel is batteries-included so everyone can{' '}<span className="hero-subtitle-br" />build and ship web apps at ridiculous speed.
            </p>
            <div className="hero-buttons">
              <a href="/docs/12.x" className="hero-btn-secondary">
                View framework docs
              </a>
            </div>
          </div>
        </section>

        {/* child 2: illustration overlay */}
        <div
          className="hero-illustration-wrapper"
          aria-hidden="true"
        >
          {svgContent ? (
            <div
              ref={svgRef}
              className="hero-illustration-svg"
              dangerouslySetInnerHTML={{__html: svgContent}}
            />
          ) : (
            <img
              className="hero-illustration-svg"
              src="/images/home/hero-illustration.png"
              alt=""
            />
          )}
        </div>

        {/* child 3: grain noise overlay */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
          className="hero-grain-overlay"
          width="100%"
          height="100%"
          preserveAspectRatio="none"
        >
          <defs>
            <filter id="hero-noise-filter">
              <feTurbulence type="turbulence" baseFrequency="3" numOctaves="1" stitchTiles="stitch" result="noise" />
              <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.8 0" result="coloredNoise" />
            </filter>
          </defs>
          <rect width="100%" height="100%" filter="url(#hero-noise-filter)" />
        </svg>
      </div>

    </header>
  );
}
