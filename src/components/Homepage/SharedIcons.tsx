import React, {useId, type ReactNode} from 'react';

export function CheckIcon({className = 'check-icon'}: {className?: string}): ReactNode {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="18" height="18" className={className} aria-hidden="true">
      <path fill="currentColor" fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clipRule="evenodd" />
    </svg>
  );
}

export function ArrowIcon({className = 'cloud-arrow-icon'}: {className?: string}): ReactNode {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className={className}>
      <path fillRule="evenodd" d="M5.22 14.78a.75.75 0 0 0 1.06 0l7.22-7.22v5.69a.75.75 0 0 0 1.5 0v-7.5a.75.75 0 0 0-.75-.75h-7.5a.75.75 0 0 0 0 1.5h5.69l-7.22 7.22a.75.75 0 0 0 0 1.06Z" clipRule="evenodd" />
    </svg>
  );
}

export function NoiseOverlay({className}: {className?: string}): ReactNode {
  const id = useId();
  const filterId = `noise-filter-${id}`;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      className={className}
      width="100%"
      height="100%"
      preserveAspectRatio="none"
    >
      <defs>
        <filter id={filterId}>
          <feTurbulence
            type="turbulence"
            baseFrequency="3"
            numOctaves="1"
            stitchTiles="stitch"
            result="noise"
          />
          <feColorMatrix
            type="matrix"
            values="0 0 0 0 0
                    0 0 0 0 0
                    0 0 0 0 0
                    0 0 0 3 0"
            result="coloredNoise"
          />
        </filter>
      </defs>
      <rect width="100%" height="100%" filter={`url(#${filterId})`} />
    </svg>
  );
}
