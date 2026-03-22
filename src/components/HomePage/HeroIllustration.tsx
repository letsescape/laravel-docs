import React, {useEffect, useRef, type ReactNode} from 'react';
import styles from './HeroIllustration.module.css';

// Color for each icon (used to tint the 3D block top face)
const iconColors = [
  '#171717', // 0: OpenAI
  '#2563EB', // 1: Gemini
  '#d97757', // 2: Livewire
  '#4E243D', // 3: Laravel
  '#a7ebcc', // 4: Vue
  '#0a6890', // 5: React
  '#FE640B', // 6: Svelte
];

// Icon SVG strings for each framework (used to swap top-block icons)
const icons = [
  // 0: OpenAI
  {
    left: `<svg viewBox="0 0 16 16" fill="none" height="32"><path d="M6.183 9.049V3.853l3.311-1.912c1.435-.828 3.27-.337 4.098 1.098.554.96.518 2.099.003 2.995" stroke="white" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 5.902l4.5 2.598v3.823c0 1.657-1.343 3-3 3-1.108 0-2.076-.601-2.596-1.495" stroke="white" stroke-linecap="round" stroke-linejoin="round"/><path d="M9.817 9.049l-4.5 2.598-3.311-1.912c-1.435-.828-1.927-2.663-1.098-4.098.554-.96 1.559-1.498 2.592-1.5" stroke="white" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 10.098l-4.5-2.598V3.677c0-1.657 1.343-3 3-3 1.108 0 2.076.601 2.596 1.495" stroke="white" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.183 6.951l4.5-2.598 3.311 1.912c1.435.828 1.927 2.663 1.098 4.098-.554.96-1.559 1.498-2.592 1.5" stroke="white" stroke-linecap="round" stroke-linejoin="round"/><path d="M9.817 6.951v5.196l-3.311 1.912c-1.435.828-3.27.337-4.098-1.098-.554-.96-.518-2.099-.003-2.995" stroke="white" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    right: `<svg viewBox="0 0 16 16" fill="none" height="24"><path d="M6.183 9.049V3.853l3.311-1.912c1.435-.828 3.27-.337 4.098 1.098.554.96.518 2.099.003 2.995" stroke="black" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 5.902l4.5 2.598v3.823c0 1.657-1.343 3-3 3-1.108 0-2.076-.601-2.596-1.495" stroke="black" stroke-linecap="round" stroke-linejoin="round"/><path d="M9.817 9.049l-4.5 2.598-3.311-1.912c-1.435-.828-1.927-2.663-1.098-4.098.554-.96 1.559-1.498 2.592-1.5" stroke="black" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 10.098l-4.5-2.598V3.677c0-1.657 1.343-3 3-3 1.108 0 2.076.601 2.596 1.495" stroke="black" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.183 6.951l4.5-2.598 3.311 1.912c1.435.828 1.927 2.663 1.098 4.098-.554.96-1.559 1.498-2.592 1.5" stroke="black" stroke-linecap="round" stroke-linejoin="round"/><path d="M9.817 6.951v5.196l-3.311 1.912c-1.435.828-3.27.337-4.098-1.098-.554-.96-.518-2.099-.003-2.995" stroke="black" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  },
  // 1: Gemini
  {
    left: `<svg fill="none" viewBox="0 0 16 16" height="32"><path d="M16 8.016A8.522 8.522 0 008.016 16h-.032A8.521 8.521 0 000 8.016v-.032A8.521 8.521 0 007.984 0h.032A8.522 8.522 0 0016 7.984v.032z" fill="white"/></svg>`,
    right: `<svg fill="none" viewBox="0 0 16 16" height="24"><path d="M16 8.016A8.522 8.522 0 008.016 16h-.032A8.521 8.521 0 000 8.016v-.032A8.521 8.521 0 007.984 0h.032A8.522 8.522 0 0016 7.984v.032z" fill="white"/></svg>`,
  },
  // 2: Livewire
  {
    left: `<svg viewBox="0 0 17 16" fill="none" height="32"><path fill-rule="evenodd" clip-rule="evenodd" d="M3.639 10.637L6.786 8.872l.053-.153-.053-.086h-.153l-.526-.032-1.799-.048-1.559-.065-1.511-.081-.38-.081L.5 7.856l.037-.235.32-.214.457.04 1.013.069 1.519.105 1.101.065 1.633.17h.26l.036-.105-.089-.065-.069-.065-1.572-1.064-1.701-1.126-.891-.648-.483-.327-.242-.308-.106-.672.438-.481.587.04.15.04.596.458 1.272.984 1.66 1.222.244.203.097-.069.012-.048-.109-.183-.903-1.631-.964-1.66-.43-.688-.113-.413A2.08 2.08 0 014.19.765l.499-.676L4.964 0l.664.089.28.243.413.943.668 1.486 1.037 2.02.304.599.162.555.06.17h.106v-.098l.085-1.137.158-1.397.153-1.797.054-.506.25-.607.498-.328.39.187.32.457-.045.296-.19 1.234-.373 1.935-.242 1.295h.141l.162-.161.657-.871 1.101-1.376.487-.547.567-.602.364-.288h.689l.507.753-.227.777-.71.898-.587.761-.843 1.134-.526.906.048.074.126-.014 1.904-.404 1.029-.187 1.227-.21.556.259.06.263-.218.538-1.313.324-1.539.308-2.293.542-.028.02.033.04 1.033.098.441.024h1.082l2.013.15.527.348.316.425-.053.324-.81.413-1.093-.259-2.553-.607-.875-.22h-.121v.074l.729.712 1.337 1.207 1.673 1.553.085.385-.214.304-.227-.033-1.47-1.105-.567-.498-1.284-1.08h-.085v.114l.296.432 1.563 2.348.081.72-.113.235-.406.142-.445-.081-.916-1.284-.943-1.444-.762-1.296-.094.054-.45 4.836-.21.247-.486.187-.405-.308-.214-.498.214-.984.26-1.283.21-1.02.19-1.266.114-.422-.008-.028-.094.012-.956 1.311-1.453 1.964-1.151 1.23-.276.109-.478-.247.045-.441.268-.393 1.591-2.024.96-1.254.62-.724-.004-.105h-.037l-4.229 2.744-.753.098-.325-.304.041-.498.154-.162 1.272-.874z" fill="white"/></svg>`,
    right: `<svg viewBox="0 0 17 16" fill="none" height="24"><path fill-rule="evenodd" clip-rule="evenodd" d="M3.639 10.637L6.786 8.872l.053-.153-.053-.086h-.153l-.526-.032-1.799-.048-1.559-.065-1.511-.081-.38-.081L.5 7.856l.037-.235.32-.214.457.04 1.013.069 1.519.105 1.101.065 1.633.17h.26l.036-.105-.089-.065-.069-.065-1.572-1.064-1.701-1.126-.891-.648-.483-.327-.242-.308-.106-.672.438-.481.587.04.15.04.596.458 1.272.984 1.66 1.222.244.203.097-.069.012-.048-.109-.183-.903-1.631-.964-1.66-.43-.688-.113-.413A2.08 2.08 0 014.19.765l.499-.676L4.964 0l.664.089.28.243.413.943.668 1.486 1.037 2.02.304.599.162.555.06.17h.106v-.098l.085-1.137.158-1.397.153-1.797.054-.506.25-.607.498-.328.39.187.32.457-.045.296-.19 1.234-.373 1.935-.242 1.295h.141l.162-.161.657-.871 1.101-1.376.487-.547.567-.602.364-.288h.689l.507.753-.227.777-.71.898-.587.761-.843 1.134-.526.906.048.074.126-.014 1.904-.404 1.029-.187 1.227-.21.556.259.06.263-.218.538-1.313.324-1.539.308-2.293.542-.028.02.033.04 1.033.098.441.024h1.082l2.013.15.527.348.316.425-.053.324-.81.413-1.093-.259-2.553-.607-.875-.22h-.121v.074l.729.712 1.337 1.207 1.673 1.553.085.385-.214.304-.227-.033-1.47-1.105-.567-.498-1.284-1.08h-.085v.114l.296.432 1.563 2.348.081.72-.113.235-.406.142-.445-.081-.916-1.284-.943-1.444-.762-1.296-.094.054-.45 4.836-.21.247-.486.187-.405-.308-.214-.498.214-.984.26-1.283.21-1.02.19-1.266.114-.422-.008-.028-.094.012-.956 1.311-1.453 1.964-1.151 1.23-.276.109-.478-.247.045-.441.268-.393 1.591-2.024.96-1.254.62-.724-.004-.105h-.037l-4.229 2.744-.753.098-.325-.304.041-.498.154-.162 1.272-.874z" fill="white"/></svg>`,
  },
  // 3: Laravel (pink blob)
  {
    left: `<svg viewBox="-4 -2 36 32" fill="none" height="46"><path fill-rule="evenodd" clip-rule="evenodd" d="M24.977 22.47c-.453.685-.797 1.53-1.718 1.53-1.55 0-1.634-2.392-3.186-2.392s-1.483 2.392-3.034 2.392-1.118-2.392-2.67-2.392-1.483 2.392-3.034 2.392-1.635-2.392-3.187-2.392-1.483 2.392-3.034 2.392c-.487 0-.83-.236-1.119-.56A10.833 10.833 0 011.778 16.826c0-7.084 5.472-12.826 12.222-12.826s12.222 5.742 12.222 12.826c0 2.025-.448 3.94-1.245 5.644z" fill="#FB70A9"/><path fill-rule="evenodd" clip-rule="evenodd" d="M13.346 20.024c4.25 0 6.04-2.466 6.04-5.967 0-3.503-2.704-6.725-6.04-6.725s-6.04 3.223-6.04 6.725c0 3.502 1.789 5.967 6.04 5.967z" fill="white"/><path d="M11.722 14.258c1.25 0 2.265-1.12 2.265-2.5s-1.014-2.5-2.265-2.5-2.265 1.12-2.265 2.5 1.014 2.5 2.265 2.5z" fill="#030776"/></svg>`,
    right: `<svg viewBox="-4 -2 36 32" fill="none" height="36"><path fill-rule="evenodd" clip-rule="evenodd" d="M24.977 22.47c-.453.685-.797 1.53-1.718 1.53-1.55 0-1.634-2.392-3.186-2.392s-1.483 2.392-3.034 2.392-1.118-2.392-2.67-2.392-1.483 2.392-3.034 2.392-1.635-2.392-3.187-2.392-1.483 2.392-3.034 2.392c-.487 0-.83-.236-1.119-.56A10.833 10.833 0 011.778 16.826c0-7.084 5.472-12.826 12.222-12.826s12.222 5.742 12.222 12.826c0 2.025-.448 3.94-1.245 5.644z" fill="#FB70A9"/><path fill-rule="evenodd" clip-rule="evenodd" d="M13.346 20.024c4.25 0 6.04-2.466 6.04-5.967 0-3.503-2.704-6.725-6.04-6.725s-6.04 3.223-6.04 6.725c0 3.502 1.789 5.967 6.04 5.967z" fill="white"/><path d="M11.722 14.258c1.25 0 2.265-1.12 2.265-2.5s-1.014-2.5-2.265-2.5-2.265 1.12-2.265 2.5 1.014 2.5 2.265 2.5z" fill="#030776"/></svg>`,
  },
  // 4: Vue
  {
    left: `<svg viewBox="-4 -2 36 32" fill="none" height="46"><path d="M16.663 4.001L14 8.62l-2.663-4.619H2.468L14 24l11.533-19.999h-8.87z" fill="#41B883"/><path d="M16.664 4.001L14 8.62l-2.663-4.619H7.081L14 16l6.92-11.999h-4.256z" fill="#34495E"/></svg>`,
    right: `<svg viewBox="-4 -2 36 32" fill="none" height="36"><path d="M16.663 4.001L14 8.62l-2.663-4.619H2.468L14 24l11.533-19.999h-8.87z" fill="#41B883"/><path d="M16.664 4.001L14 8.62l-2.663-4.619H7.081L14 16l6.92-11.999h-4.256z" fill="#34495E"/></svg>`,
  },
  // 5: React
  {
    left: `<svg viewBox="-4 -2 36 32" fill="none" height="46"><circle cx="14" cy="14" r="2.5" fill="white"/><ellipse cx="14" cy="14" rx="11" ry="4.5" stroke="white" stroke-width="0.8"/><ellipse cx="14" cy="14" rx="11" ry="4.5" transform="rotate(60 14 14)" stroke="white" stroke-width="0.8"/><ellipse cx="14" cy="14" rx="11" ry="4.5" transform="rotate(120 14 14)" stroke="white" stroke-width="0.8"/></svg>`,
    right: `<svg viewBox="-4 -2 36 32" fill="none" height="36"><circle cx="14" cy="14" r="2.5" fill="white"/><ellipse cx="14" cy="14" rx="11" ry="4.5" stroke="white" stroke-width="0.8"/><ellipse cx="14" cy="14" rx="11" ry="4.5" transform="rotate(60 14 14)" stroke="white" stroke-width="0.8"/><ellipse cx="14" cy="14" rx="11" ry="4.5" transform="rotate(120 14 14)" stroke="white" stroke-width="0.8"/></svg>`,
  },
  // 6: Svelte
  {
    left: `<svg viewBox="-4 -2 36 32" fill="none" height="46"><path d="M21.439 12.091s2.127-3.031.122-5.924c-2.531-3.195-5.357-1.913-5.357-1.913s-5.036 2.678-7.821 4.576c-2.143 1.531-3.429 3.459-1.577 6.689 1.868 3.214 7.01 1.852 7.01 1.852" stroke="white" stroke-width="0.7" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.562 16.008s-2.128 3.031-.122 5.924 5.357 1.913 5.357 1.913 5.035-2.663 7.821-4.561c2.143-1.531 3.429-3.459 1.577-6.689-1.868-3.214-7.01-1.852-7.01-1.852M11.399 12.457l6.336-3.918M10.205 19.636l6.336-3.904" stroke="white" stroke-width="0.7" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    right: `<svg viewBox="-4 -2 36 32" fill="none" height="36"><path d="M21.439 12.091s2.127-3.031.122-5.924c-2.531-3.195-5.357-1.913-5.357-1.913s-5.036 2.678-7.821 4.576c-2.143 1.531-3.429 3.459-1.577 6.689 1.868 3.214 7.01 1.852 7.01 1.852" stroke="white" stroke-width="0.7" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.562 16.008s-2.128 3.031-.122 5.924 5.357 1.913 5.357 1.913 5.035-2.663 7.821-4.561c2.143-1.531 3.429-3.459 1.577-6.689-1.868-3.214-7.01-1.852-7.01-1.852M11.399 12.457l6.336-3.918M10.205 19.636l6.336-3.904" stroke="white" stroke-width="0.7" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  },
];

export default function HeroIllustration(): ReactNode {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    fetch('/img/hero-illustration.svg')
      .then(res => res.text())
      .then(svgText => {
        el.innerHTML = svgText;
        const svg = el.querySelector('svg');
        if (!svg) return;

        svg.style.width = '100%';
        svg.style.height = '100%';

        // Force inline styles on all elements with fill/stroke attributes
        // to override the global CSS rule that sets fill:none !important
        svg.querySelectorAll('[fill]').forEach(el => {
          const fill = el.getAttribute('fill');
          if (fill && fill !== 'none') {
            (el as HTMLElement).style.setProperty('fill', fill, 'important');
          }
        });
        svg.querySelectorAll('[stroke]').forEach(el => {
          const stroke = el.getAttribute('stroke');
          if (stroke) {
            (el as HTMLElement).style.setProperty('stroke', stroke, 'important');
          }
        });

        // Find marked elements
        const leftSlot = svg.querySelector('[data-icon-slot="left"]');
        const rightSlot = svg.querySelector('[data-icon-slot="right"]');
        const bottomIcons = svg.querySelectorAll('[data-bottom-icon]');

        // Set default icons: OpenAI (0) for right slot, Laravel (3) for left slot
        const applyIcon = (idx: number) => {
          const icon = icons[idx];
          const color = iconColors[idx];
          if (!icon) return;
          if (idx <= 2) {
            if (rightSlot) {
              rightSlot.querySelectorAll(':scope > g').forEach((g) => { g.innerHTML = icon.left; });
            }
            svg.querySelectorAll('[data-block-face^="right-"]').forEach((face) => {
              face.setAttribute('fill', color);
              (face as HTMLElement).style.setProperty('fill', color, 'important');
            });
          } else {
            if (leftSlot) {
              leftSlot.querySelectorAll(':scope > g').forEach((g) => { g.innerHTML = icon.left; });
            }
            svg.querySelectorAll('[data-block-face^="left-"]').forEach((face) => {
              face.setAttribute('fill', color);
              (face as HTMLElement).style.setProperty('fill', color, 'important');
            });
          }
        };
        const reapplyStyles = () => {
          el.querySelectorAll('[fill]').forEach(e => {
            const fill = e.getAttribute('fill');
            if (fill && fill !== 'none') (e as HTMLElement).style.setProperty('fill', fill, 'important');
          });
          el.querySelectorAll('[stroke]').forEach(e => {
            const stroke = e.getAttribute('stroke');
            if (stroke) (e as HTMLElement).style.setProperty('stroke', stroke, 'important');
          });
        };

        applyIcon(0); // OpenAI → right slot
        applyIcon(3); // Laravel → left slot
        reapplyStyles();

        // Block face: smooth fill color morph. Icons swap instantly.
        if (!document.getElementById('hero-icon-anim')) {
          const style = document.createElement('style');
          style.id = 'hero-icon-anim';
          style.textContent = `
            [data-block-face] { transition: fill 500ms ease-in-out !important; }
            [data-bottom-tile] { transition: transform 0.15s linear !important; }
          `;
          document.head.appendChild(style);
        }

        const applyIconAnimated = (idx: number) => {
          applyIcon(idx);
          reapplyStyles();
        };

        // Step vector between icon positions
        const stepX = 39.8485383043;
        const stepY = -23.004861655600003;

        // Tile positions relative to base (icon 2 position = step 0)
        // "left" tile cycles icons 0,1,2 → steps -2,-1,0
        // "right" tile cycles icons 3,4,5,6 → steps 1,2,3,4
        const leftTile = svg.querySelector('[data-bottom-tile="left"]') as HTMLElement;
        const rightTile = svg.querySelector('[data-bottom-tile="right"]') as HTMLElement;

        const leftSteps = [-2, -1, 0];   // icon 0, 1, 2
        const rightSteps = [1, 2, 3, 4]; // icon 3, 4, 5, 6

        let leftTileIdx = 0;  // starts at icon 0 (step -2)
        let rightTileIdx = 0; // starts at icon 3 (step 1)

        const moveTile = (tile: HTMLElement, step: number) => {
          const tx = step * stepX;
          const ty = step * stepY;
          tile.style.transform = `translate(${tx}px, ${ty}px)`;
        };

        // Auto-rotate icons every 2 seconds, synced with tile movement
        const rightIcons = [0, 1, 2];
        const leftIcons = [3, 4, 5, 6];
        let rightIdx = 0;
        let leftIdx = 0;

        const interval = setInterval(() => {
          // Move tiles simultaneously
          rightTileIdx = (rightTileIdx + 1) % rightSteps.length;
          leftTileIdx = (leftTileIdx + 1) % leftSteps.length;
          if (rightTile) moveTile(rightTile, rightSteps[rightTileIdx]);
          if (leftTile) moveTile(leftTile, leftSteps[leftTileIdx]);

          // Rotate block icons in sync
          rightIdx = (rightIdx + 1) % rightIcons.length;
          leftIdx = (leftIdx + 1) % leftIcons.length;
          applyIconAnimated(rightIcons[rightIdx]);
          applyIconAnimated(leftIcons[leftIdx]);
        }, 2500);

        // Cleanup on unmount
        (el as any).__iconInterval = interval;

        bottomIcons.forEach((rect) => {
          const r = rect as SVGRectElement;
          r.style.cursor = 'pointer';
          r.style.transition = 'fill 0.2s';
          r.setAttribute('pointer-events', 'all');

          r.addEventListener('mouseenter', () => { r.setAttribute('fill', 'rgba(255,255,255,0.7)'); });
          r.addEventListener('mouseleave', () => { r.setAttribute('fill', 'transparent'); });

          r.addEventListener('click', () => {
            const idx = parseInt(r.getAttribute('data-bottom-icon') || '0', 10);
            const icon = icons[idx];
            if (!icon) return;

            const color = iconColors[idx];

            if (idx <= 2) {
              // Icons 0-2 (OpenAI, Gemini, Livewire) change the RIGHT slot (3 small icons)
              if (rightSlot) {
                const gs = rightSlot.querySelectorAll(':scope > g');
                gs.forEach((g) => {
                  g.innerHTML = icon.left;
                });
              }
              // Change the right block face colors
              svg.querySelectorAll('[data-block-face^="right-"]').forEach((face) => {
                face.setAttribute('fill', color);
                (face as HTMLElement).style.setProperty('fill', color, 'important');
              });
            } else {
              // Icons 3-6 (Laravel, Vue, React, Svelte) change the LEFT slot (large icons)
              if (leftSlot) {
                const gs = leftSlot.querySelectorAll(':scope > g');
                gs.forEach((g) => {
                  g.innerHTML = icon.left;
                });
              }
              // Change the left block face colors
              svg.querySelectorAll('[data-block-face^="left-"]').forEach((face) => {
                face.setAttribute('fill', color);
                (face as HTMLElement).style.setProperty('fill', color, 'important');
              });
            }

            // Re-apply inline styles to new elements
            const container = containerRef.current;
            if (container) {
              container.querySelectorAll('[fill]').forEach(el => {
                const fill = el.getAttribute('fill');
                if (fill && fill !== 'none') {
                  (el as HTMLElement).style.setProperty('fill', fill, 'important');
                }
              });
              container.querySelectorAll('[stroke]').forEach(el => {
                const stroke = el.getAttribute('stroke');
                if (stroke) {
                  (el as HTMLElement).style.setProperty('stroke', stroke, 'important');
                }
              });
            }
          });
        });
      });
    return () => {
      const el = containerRef.current;
      if (el && (el as any).__iconInterval) {
        clearInterval((el as any).__iconInterval);
      }
    };
  }, []);

  return <div ref={containerRef} className={`${styles.wrapper} hero-illustration`} />;
}
