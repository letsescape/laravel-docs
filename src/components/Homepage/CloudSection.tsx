import React, {useState, useEffect, type ReactNode} from 'react';

function CheckIcon(): ReactNode {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" className="cloud-check-icon">
      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clipRule="evenodd" />
    </svg>
  );
}

function ArrowIcon(): ReactNode {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="cloud-arrow-icon">
      <path fillRule="evenodd" d="M5.22 14.78a.75.75 0 0 0 1.06 0l7.22-7.22v5.69a.75.75 0 0 0 1.5 0v-7.5a.75.75 0 0 0-.75-.75h-7.5a.75.75 0 0 0 0 1.5h5.69l-7.22 7.22a.75.75 0 0 0 0 1.06Z" clipRule="evenodd" />
    </svg>
  );
}

function IdlingIcon(): ReactNode {
  return (
    <svg viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg" className="badge-icon">
      <path fillRule="evenodd" clipRule="evenodd" d="M12.75 3.75c0 .54-.286 1.012-.714 1.276A6.125 6.125 0 1 1 8.151.843 1.5 1.5 0 0 1 9.5 0h1.75a1.5 1.5 0 0 1 1.184 2.42l-.173.224c.3.273.489.667.489 1.106" fill="#2563eb" />
      <path d="M9.5 1a.5.5 0 0 0 0 1zm1.75.5.395.307A.5.5 0 0 0 11.25 1zM9.5 3.75l-.395-.307a.5.5 0 0 0 .395.807zm1.75.5a.5.5 0 0 0 0-1zm-4.625.25a.5.5 0 0 0-1 0zm-.5 2.125h-.5a.5.5 0 0 0 .146.354zm.896 1.604a.5.5 0 1 0 .708-.708l-.354.354zm.665-5.424a.5.5 0 1 0 .378-.925l-.189.463zM11.06 5.24a.5.5 0 0 0-.963.27l.481-.135zM9.5 1.5V2h1.75V1H9.5zm1.75 0-.395-.307-1.75 2.25.395.307.395.307 1.75-2.25zM9.5 3.75v.5h1.75v-1H9.5zm-3.375.75h-.5v2.125h1V4.5zm0 2.125-.354.354 1.25 1.25.354-.354.354-.354-1.25-1.25zm4.625 0h-.5a4.125 4.125 0 0 1-4.125 4.125v1a5.125 5.125 0 0 0 5.125-5.125zM6.125 11.25v-.5A4.125 4.125 0 0 1 2 6.625H1a5.125 5.125 0 0 0 5.125 5.125zM1.5 6.625H2A4.125 4.125 0 0 1 6.125 2.5v-1A5.125 5.125 0 0 0 1 6.625zM6.125 2v.5c.553 0 1.08.109 1.56.305l.19-.462.19-.463a5.1 5.1 0 0 0-1.94-.38zm4.454 3.375-.481.135q.15.533.152 1.115h1c0-.48-.066-.944-.19-1.385z" fill="#fff" />
    </svg>
  );
}

function ScalingUpIcon(): ReactNode {
  return (
    <svg viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg" className="badge-icon">
      <path d="M5.824 3.19a.458.458 0 0 0-.648 0L3.19 5.176a.458.458 0 0 0 .648.648L5.042 4.62v5.31a.458.458 0 0 0 .916 0V4.62l1.204 1.204a.458.458 0 0 0 .648-.648L5.824 3.19Z" fill="#059669" />
      <path d="M1.986 1.528a.458.458 0 0 0-.917 0v.458a.458.458 0 0 0 .917 0v-.458Zm1.833 0a.458.458 0 1 0-.916 0v.458a.458.458 0 0 0 .916 0v-.458Zm1.834 0a.458.458 0 0 0-.917 0v.458a.458.458 0 0 0 .917 0v-.458Zm1.833 0a.458.458 0 1 0-.916 0v.458a.458.458 0 0 0 .916 0v-.458Zm1.834 0a.458.458 0 0 0-.917 0v.458a.458.458 0 0 0 .917 0v-.458Z" fill="#059669" />
    </svg>
  );
}

function ScalingDownIcon(): ReactNode {
  return (
    <svg viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg" className="badge-icon">
      <path d="M5.176 7.81a.458.458 0 0 0 .648 0l1.986-1.986a.458.458 0 0 0-.648-.648L5.958 6.38V1.069a.458.458 0 0 0-.916 0V6.38L3.838 5.176a.458.458 0 0 0-.648.648L5.176 7.81Z" fill="#F59E0B" />
      <path d="M1.986 9.472a.458.458 0 0 0-.917 0v.458a.458.458 0 0 0 .917 0v-.458Zm1.833 0a.458.458 0 1 0-.916 0v.458a.458.458 0 0 0 .916 0v-.458Zm1.834 0a.458.458 0 0 0-.917 0v.458a.458.458 0 0 0 .917 0v-.458Zm1.833 0a.458.458 0 1 0-.916 0v.458a.458.458 0 0 0 .916 0v-.458Zm1.834 0a.458.458 0 0 0-.917 0v.458a.458.458 0 0 0 .917 0v-.458Z" fill="#F59E0B" />
    </svg>
  );
}

const BADGES = [
  {label: 'Idling', icon: <IdlingIcon />, accent: '#2563EB99'},
  {label: 'Scaling up', icon: <ScalingUpIcon />, accent: '#05966999'},
  {label: 'Scaling down', icon: <ScalingDownIcon />, accent: '#F59E0B99'},
] as const;

function AutoscaleIllustration(): ReactNode {
  const [activeIdx, setActiveIdx] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveIdx(prev => (prev + 1) % BADGES.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="cloud-illust-wrapper" aria-hidden="true">
      <div className="cloud-illust-inner">
        {/* Animated status badges */}
        <div className="cloud-badge-container">
          {BADGES.map((badge, idx) => (
            <div
              key={badge.label}
              className={`cloud-status-badge ${idx === activeIdx ? 'cloud-status-badge--active' : ''}`}
              style={{'--badge-accent': badge.accent} as React.CSSProperties}
            >
              {badge.icon}
              {badge.label}
            </div>
          ))}
        </div>

        {/* Main SVG illustration - dashboard mockup with arc lines */}
        <svg
          viewBox="0 0 748 274"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="cloud-dashboard-svg"
        >
          {/* Dashed arc lines */}
          <g>
            <path id="cloud-arc-0" d="M0 23.6289L28.3214 57.3595C46.5617 79.0838 73.4759 91.6289 101.842 91.6289H646.158C674.524 91.6289 701.438 79.0838 719.679 57.3595L748 23.6289" stroke="#E5E5E5" strokeDasharray="3 3" className="cloud-dash-line" />
            <path id="cloud-arc-1" d="M0 66.6289L31.1946 90.6688C47.9879 103.61 68.5929 110.629 89.7943 110.629H658.206C679.407 110.629 700.012 103.61 716.805 90.6688L748 66.6289" stroke="#E5E5E5" strokeDasharray="3 3" className="cloud-dash-line" />
            <path id="cloud-arc-2" d="M0 109.629L41.6855 124.231C51.8853 127.804 62.6152 129.629 73.4228 129.629H674.577C685.385 129.629 696.115 127.804 706.315 124.231L748 109.629" stroke="#E5E5E5" strokeDasharray="3 3" className="cloud-dash-line" />
            <path id="cloud-arc-3" d="M0 148.625L748 148.627" stroke="#E5E5E5" strokeDasharray="3 3" className="cloud-dash-line" />
            <path id="cloud-arc-4" d="M0 186.629L41.6855 172.027C51.8853 168.454 62.6152 166.629 73.4228 166.629H674.577C685.385 166.629 696.115 168.454 706.315 172.027L748 186.629" stroke="#E5E5E5" strokeDasharray="3 3" className="cloud-dash-line" />
            <path id="cloud-arc-5" d="M0 229.629L31.1946 205.589C47.9879 192.647 68.5929 185.629 89.7943 185.629H658.206C679.407 185.629 700.012 192.647 716.805 205.589L748 229.629" stroke="#E5E5E5" strokeDasharray="3 3" className="cloud-dash-line" />
            <path id="cloud-arc-6" d="M0 272.629L28.3214 238.898C46.5617 217.174 73.4759 204.629 101.842 204.629H646.158C674.524 204.629 701.438 217.174 719.679 238.898L748 272.629" stroke="#E5E5E5" strokeDasharray="3 3" className="cloud-dash-line" />
          </g>

          {/* Animated colored dots moving along dashed arc paths */}
          <g className="cloud-dots">
            {/* Dot on arc line 3 (path index 2) - green */}
            <circle r="6" fill="url(#cloud-dot-green)" className="cloud-dot-moving">
              <animateMotion dur="8s" repeatCount="indefinite" begin="0s">
                <mpath xlinkHref="#cloud-arc-2" />
              </animateMotion>
              <animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.5;0.95;1" dur="8s" repeatCount="indefinite" begin="0s" />
            </circle>
            {/* Dot on arc line 4 (straight) - blue */}
            <circle r="6" fill="url(#cloud-dot-blue)" className="cloud-dot-moving">
              <animateMotion dur="7s" repeatCount="indefinite" begin="1s">
                <mpath xlinkHref="#cloud-arc-3" />
              </animateMotion>
              <animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.5;0.95;1" dur="7s" repeatCount="indefinite" begin="1s" />
            </circle>
            {/* Dot on arc line 5 - amber */}
            <circle r="6" fill="url(#cloud-dot-amber)" className="cloud-dot-moving">
              <animateMotion dur="9s" repeatCount="indefinite" begin="2s">
                <mpath xlinkHref="#cloud-arc-4" />
              </animateMotion>
              <animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.5;0.95;1" dur="9s" repeatCount="indefinite" begin="2s" />
            </circle>
            {/* Dot on arc line 6 - green */}
            <circle r="6" fill="url(#cloud-dot-green)" className="cloud-dot-moving">
              <animateMotion dur="10s" repeatCount="indefinite" begin="0.5s">
                <mpath xlinkHref="#cloud-arc-5" />
              </animateMotion>
              <animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.5;0.95;1" dur="10s" repeatCount="indefinite" begin="0.5s" />
            </circle>
            {/* Dot on arc line 7 - amber */}
            <circle r="6" fill="url(#cloud-dot-amber)" className="cloud-dot-moving">
              <animateMotion dur="11s" repeatCount="indefinite" begin="3s">
                <mpath xlinkHref="#cloud-arc-6" />
              </animateMotion>
              <animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.5;0.95;1" dur="11s" repeatCount="indefinite" begin="3s" />
            </circle>
            {/* Second dot on arc line 3 - blue */}
            <circle r="6" fill="url(#cloud-dot-blue)" className="cloud-dot-moving">
              <animateMotion dur="8s" repeatCount="indefinite" begin="4s">
                <mpath xlinkHref="#cloud-arc-2" />
              </animateMotion>
              <animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.5;0.95;1" dur="8s" repeatCount="indefinite" begin="4s" />
            </circle>
          </g>

          {/* Outer card frame */}
          <path d="M260.765 52.218h225.5c11.695 0 21.175 9.48 21.175 21.176v149c0 11.694-9.48 21.175-21.175 21.175h-225.5c-11.695 0-21.176-9.481-21.176-21.175v-149c0-11.695 9.481-21.176 21.176-21.176" fill="#fefefe" />
          <path d="M260.765 52.218h225.5c11.695 0 21.175 9.48 21.175 21.176v149c0 11.694-9.48 21.175-21.175 21.175h-225.5c-11.695 0-21.176-9.481-21.176-21.175v-149c0-11.695 9.481-21.176 21.176-21.176Z" stroke="#f5f5f5" strokeWidth="1.178" />

          {/* Inner card background */}
          <path d="M266.206 63.1h214.618c8.69 0 15.734 7.045 15.735 15.735v138.118c-.001 8.69-7.045 15.734-15.735 15.735H266.206c-8.69-.001-15.734-7.045-15.734-15.735V78.835c0-8.69 7.044-15.734 15.734-15.734" fill="#fafafa" fillOpacity="0.6" />
          <path d="M266.206 63.1h214.618c8.69 0 15.734 7.045 15.735 15.735v138.118c-.001 8.69-7.045 15.734-15.735 15.735H266.206c-8.69-.001-15.734-7.045-15.734-15.735V78.835c0-8.69 7.044-15.734 15.734-15.734Z" stroke="#f5f5f5" strokeWidth="1.178" />

          {/* Main content card (left large) */}
          <g className="cloud-card-shadow">
            <path d="M271.648 73.983h127.234c5.685 0 10.294 4.61 10.294 10.294v127.235c0 5.684-4.609 10.294-10.294 10.294H271.648c-5.685 0-10.294-4.61-10.294-10.294V84.277c0-5.684 4.609-10.294 10.294-10.294" fill="#fff" />
            <path d="M271.648 73.983h127.234c5.685 0 10.294 4.61 10.294 10.294v127.235c0 5.684-4.609 10.294-10.294 10.294H271.648c-5.685 0-10.294-4.61-10.294-10.294V84.277c0-5.684 4.609-10.294 10.294-10.294Z" stroke="#e5e5e5" strokeWidth="1.178" />
          </g>

          {/* Center icon - document/file icon */}
          <path fillRule="evenodd" clipRule="evenodd" d="m357.032 151.748-14.51 14.51h-29.024v-29.02l14.51-14.509h29.024v29.023zm-29.024-20.313v2.904h17.413v17.413h2.904v-20.317zm0-2.903h23.216v23.216h2.904v-26.12h-26.12zm0 8.706v14.51h14.51v-14.51z" fill="url(#cloud-icon-gradient)" />

          {/* Corner decorative dots (star shapes) */}
          <path d="M276.462 83.723a5 5 0 1 1 0 10 5 5 0 0 1 0-10m.598 2.662c-.142-.635-1.048-.635-1.19 0a.61.61 0 0 1-.863.416c-.585-.285-1.15.423-.742.93a.61.61 0 0 1-.213.933c-.588.28-.385 1.164.266 1.161a.61.61 0 0 1 .597.748c-.148.635.668 1.028 1.072.517a.61.61 0 0 1 .957 0c.404.51 1.219.117 1.072-.517a.61.61 0 0 1 .597-.748c.651.003.853-.88.264-1.16a.61.61 0 0 1-.212-.934c.408-.507-.157-1.215-.743-.93a.61.61 0 0 1-.862-.416m-.598 116.338a5 5 0 1 1 0 10 5 5 0 0 1 0-10m.598 2.662c-.142-.635-1.048-.635-1.19 0a.61.61 0 0 1-.863.416c-.585-.285-1.15.423-.742.93a.61.61 0 0 1-.213.933c-.588.28-.385 1.164.266 1.161a.61.61 0 0 1 .597.748c-.148.634.668 1.028 1.072.517a.61.61 0 0 1 .957 0c.404.51 1.219.117 1.072-.517a.61.61 0 0 1 .597-.748c.651.003.853-.881.264-1.161a.61.61 0 0 1-.212-.933c.408-.507-.157-1.215-.743-.93a.61.61 0 0 1-.862-.416M393.462 83.723a5 5 0 1 1 0 10 5 5 0 0 1 0-10m.598 2.662c-.142-.635-1.048-.635-1.19 0a.61.61 0 0 1-.863.416c-.585-.285-1.15.423-.742.93a.61.61 0 0 1-.213.933c-.588.28-.385 1.164.266 1.161a.61.61 0 0 1 .597.748c-.148.635.668 1.028 1.072.517a.61.61 0 0 1 .957 0c.404.51 1.219.117 1.072-.517a.61.61 0 0 1 .597-.748c.651.003.853-.88.264-1.16a.61.61 0 0 1-.212-.934c.408-.507-.157-1.215-.743-.93a.61.61 0 0 1-.862-.416m-.598 116.338a5 5 0 1 1 0 10 5 5 0 0 1 0-10m.598 2.662c-.142-.635-1.048-.635-1.19 0a.61.61 0 0 1-.863.416c-.585-.285-1.15.423-.742.93a.61.61 0 0 1-.213.933c-.588.28-.385 1.164.266 1.161a.61.61 0 0 1 .597.748c-.148.634.668 1.028 1.072.517a.61.61 0 0 1 .957 0c.404.51 1.219.117 1.072-.517a.61.61 0 0 1 .597-.748c.651.003.853-.881.264-1.161a.61.61 0 0 1-.212-.933c.408-.507-.157-1.215-.743-.93a.61.61 0 0 1-.862-.416" fill="#d4d4d4" />

          {/* Binary text decorations */}
          <text fill="#d4d4d4" xmlSpace="preserve" className="cloud-mono-text" fontSize="6" letterSpacing="-.02em">
            <tspan x="290.11" y="210.2">01100010 01100101 01100101</tspan>
          </text>
          <text fill="#d4d4d4" xmlSpace="preserve" className="cloud-mono-text" fontSize="6" letterSpacing="-.02em">
            <tspan x="290.11" y="91.2">01100010 01100101 01100101</tspan>
          </text>

          {/* Top-right small card (database icon) */}
          <g className="cloud-card-shadow">
            <path d="M424.648 73.983h50.734c5.685 0 10.294 4.61 10.294 10.294v50.735c0 5.684-4.609 10.294-10.294 10.294h-50.734c-5.685 0-10.294-4.61-10.294-10.294V84.277c0-5.684 4.609-10.294 10.294-10.294" fill="#fff" />
            <path d="M424.648 73.983h50.734c5.685 0 10.294 4.61 10.294 10.294v50.735c0 5.684-4.609 10.294-10.294 10.294h-50.734c-5.685 0-10.294-4.61-10.294-10.294V84.277c0-5.684 4.609-10.294 10.294-10.294Z" stroke="#e5e5e5" strokeWidth="1.178" />
          </g>

          {/* Database icon */}
          <path d="M458.015 102.645v7c0 .58-2.803 2-8 2s-8-1.42-8-2v-7h-2v14c0 2.763 5.022 4 10 4s10-1.237 10-4v-14zm-8 16c-5.197 0-8-1.42-8-2v-4.448c1.92.985 4.965 1.448 8 1.448s6.08-.463 8-1.448v4.448c0 .58-2.803 2-8 2" fill="#d4d4d4" />
          <path d="M450.015 106.645c5.523 0 10-1.791 10-4s-4.477-4-10-4-10 1.79-10 4 4.477 4 10 4" fill="#d4d4d4" />

          {/* Top-right card corner dots */}
          <path d="M424.018 80a4.019 4.019 0 1 1-.001 8.037 4.019 4.019 0 0 1 .001-8.037m.427 1.9c-.101-.453-.748-.453-.849 0l-.07.307a.435.435 0 0 1-.615.297l-.282-.138c-.418-.203-.822.302-.53.664l.197.245a.436.436 0 0 1-.151.666l-.285.135c-.419.2-.276.83.189.828h.314a.436.436 0 0 1 .427.534l-.072.306c-.105.453.477.733.765.368l.196-.247a.435.435 0 0 1 .682 0l.196.247c.288.365.87.085.765-.368l-.071-.306a.435.435 0 0 1 .426-.535l.314.001c.465.002.609-.628.19-.828l-.285-.135a.436.436 0 0 1-.152-.666l.197-.245c.292-.362-.111-.867-.529-.664l-.283.138a.435.435 0 0 1-.615-.297zm-.427 49.395a4.018 4.018 0 1 1 0 8.036 4.018 4.018 0 0 1 0-8.036m.427 1.9c-.101-.453-.748-.453-.849 0l-.07.307a.435.435 0 0 1-.615.297l-.282-.138c-.418-.203-.822.302-.53.664l.197.245a.436.436 0 0 1-.151.666l-.285.135c-.419.2-.276.83.189.828l.314-.001a.436.436 0 0 1 .427.534l-.072.307c-.105.452.477.733.765.368l.196-.247a.435.435 0 0 1 .682 0l.196.247c.288.365.87.085.765-.368l-.071-.307a.436.436 0 0 1 .426-.534l.314.001c.465.002.609-.628.19-.828l-.285-.135a.436.436 0 0 1-.152-.666l.197-.245c.292-.362-.111-.867-.529-.664l-.283.138a.435.435 0 0 1-.615-.297zM475.312 80a4.02 4.02 0 1 1-4.018 4.019A4.02 4.02 0 0 1 475.312 80m.428 1.9c-.102-.453-.748-.453-.85 0l-.069.307a.436.436 0 0 1-.615.297l-.283-.138c-.418-.203-.821.302-.53.664l.197.245a.435.435 0 0 1-.151.666l-.284.135c-.42.2-.276.83.188.828h.315c.281-.002.49.26.426.534l-.072.306c-.105.453.478.733.766.368l.195-.247a.436.436 0 0 1 .683 0l.195.247c.288.365.871.085.766-.368l-.072-.306a.436.436 0 0 1 .426-.535l.315.001c.464.002.609-.628.189-.828l-.284-.135a.435.435 0 0 1-.152-.666l.197-.245c.291-.362-.112-.867-.529-.664l-.284.138a.435.435 0 0 1-.615-.297zm.241 50.065a4.018 4.018 0 1 1 .001 8.037 4.018 4.018 0 0 1-.001-8.037m.428 1.9c-.101-.453-.748-.453-.849 0l-.07.307a.435.435 0 0 1-.615.297l-.282-.138c-.418-.203-.822.302-.531.664l.198.245a.435.435 0 0 1-.152.666l-.284.135c-.419.2-.276.83.189.828l.314-.001a.436.436 0 0 1 .427.534l-.072.307c-.105.452.477.733.765.368l.196-.247a.435.435 0 0 1 .682 0l.196.247c.288.365.87.085.765-.368l-.071-.307a.436.436 0 0 1 .426-.534l.314.001c.465.002.609-.628.19-.828l-.285-.135a.436.436 0 0 1-.152-.666l.197-.245c.292-.362-.111-.867-.529-.664l-.283.138a.435.435 0 0 1-.615-.297z" fill="#d9d9d9" />

          {/* Bottom-right small card (settings/deploy icon) */}
          <g className="cloud-card-shadow">
            <path d="M424.648 150.483h50.734c5.685 0 10.294 4.61 10.294 10.294v50.735c0 5.684-4.609 10.294-10.294 10.294h-50.734c-5.685 0-10.294-4.61-10.294-10.294v-50.735c0-5.684 4.609-10.294 10.294-10.294" fill="#fff" />
            <path d="M424.648 150.483h50.734c5.685 0 10.294 4.61 10.294 10.294v50.735c0 5.684-4.609 10.294-10.294 10.294h-50.734c-5.685 0-10.294-4.61-10.294-10.294v-50.735c0-5.684 4.609-10.294 10.294-10.294Z" stroke="#e5e5e5" strokeWidth="1.178" />
          </g>

          {/* Deploy/settings icon (hexagon shape) */}
          <path d="M450.015 174.145v5m-10 13 4-2m16 2-4-2m-12-8 6 3 6-3m-6 3v8" stroke="#d4d4d4" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <path d="m456.015 182.145-6-3-6 3v8l6 3 6-3z" stroke="#d4d4d4" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />

          {/* Bottom-right card corner dots */}
          <path d="M424.018 157a4.018 4.018 0 1 1 0 8.037 4.018 4.018 0 0 1 0-8.037m.427 1.9c-.101-.453-.748-.453-.849 0l-.07.307a.435.435 0 0 1-.615.297l-.282-.138c-.418-.203-.822.302-.53.664l.197.245a.436.436 0 0 1-.151.666l-.285.135c-.419.2-.276.83.189.828l.314-.001a.437.437 0 0 1 .427.535l-.072.306c-.105.453.477.733.765.368l.196-.247a.435.435 0 0 1 .682 0l.196.247c.288.365.87.085.765-.368l-.071-.306a.436.436 0 0 1 .426-.535l.314.001c.465.002.609-.628.19-.828l-.285-.135a.436.436 0 0 1-.152-.666l.197-.245c.292-.362-.111-.867-.529-.664l-.283.138a.435.435 0 0 1-.615-.297zm-.427 49.395a4.018 4.018 0 1 1 0 8.036 4.018 4.018 0 0 1 0-8.036m.427 1.9c-.101-.453-.748-.453-.849 0l-.07.307a.435.435 0 0 1-.615.297l-.282-.138c-.418-.203-.822.302-.53.664l.197.245a.436.436 0 0 1-.151.666l-.285.135c-.419.2-.276.83.189.828l.314-.001a.436.436 0 0 1 .427.534l-.072.307c-.105.452.477.733.765.368l.196-.247a.435.435 0 0 1 .682 0l.196.247c.288.365.87.085.765-.368l-.071-.307a.436.436 0 0 1 .426-.534l.314.001c.465.002.609-.628.19-.828l-.285-.135a.436.436 0 0 1-.152-.666l.197-.245c.292-.362-.111-.867-.529-.664l-.283.138a.435.435 0 0 1-.615-.297zM475.312 157a4.02 4.02 0 1 1 0 8.038 4.02 4.02 0 0 1 0-8.038m.428 1.9c-.102-.453-.748-.453-.85 0l-.069.307a.436.436 0 0 1-.615.297l-.283-.138c-.418-.203-.821.302-.53.664l.197.245a.435.435 0 0 1-.151.666l-.284.135c-.42.2-.276.83.188.828l.315-.001a.436.436 0 0 1 .426.535l-.072.306c-.105.453.478.733.766.368l.195-.247a.436.436 0 0 1 .683 0l.195.247c.288.365.871.085.766-.368l-.072-.306a.437.437 0 0 1 .426-.535l.315.001c.464.002.609-.628.189-.828l-.284-.135a.435.435 0 0 1-.152-.666l.197-.245c.291-.362-.112-.867-.529-.664l-.284.138a.436.436 0 0 1-.615-.297zm.241 50.065a4.018 4.018 0 1 1 .001 8.037 4.018 4.018 0 0 1-.001-8.037m.428 1.9c-.101-.453-.748-.453-.849 0l-.07.307a.435.435 0 0 1-.615.297l-.282-.138c-.418-.203-.822.302-.531.664l.198.245a.435.435 0 0 1-.152.666l-.284.135c-.419.2-.276.83.189.828l.314-.001a.436.436 0 0 1 .427.534l-.072.307c-.105.452.477.733.765.368l.196-.247a.435.435 0 0 1 .682 0l.196.247c.288.365.87.085.765-.368l-.071-.307a.436.436 0 0 1 .426-.534l.314.001c.465.002.609-.628.19-.828l-.285-.135a.436.436 0 0 1-.152-.666l.197-.245c.292-.362-.111-.867-.529-.664l-.283.138a.435.435 0 0 1-.615-.297z" fill="#d9d9d9" />

          <defs>
            <linearGradient id="cloud-icon-gradient" x1="335.265" y1="122.729" x2="335.265" y2="166.258" gradientUnits="userSpaceOnUse">
              <stop stopColor="#707070" />
              <stop offset="1" stopColor="#0a0a0a" />
            </linearGradient>
            <radialGradient id="cloud-dot-amber">
              <stop offset="0%" stopColor="#d97706" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#d97706" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#d97706" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="cloud-dot-blue">
              <stop offset="0%" stopColor="#2563eb" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#2563eb" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#2563eb" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="cloud-dot-green">
              <stop offset="0%" stopColor="#16a34a" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#16a34a" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#16a34a" stopOpacity="0" />
            </radialGradient>
          </defs>
        </svg>

        {/* Grain/noise overlay */}
        <svg width="100%" height="100%" className="cloud-grain-overlay">
          <filter id="cloud-grain-filter">
            <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="4" stitchTiles="stitch" />
          </filter>
          <rect width="100%" height="100%" filter="url(#cloud-grain-filter)" opacity="0.04" />
        </svg>
      </div>
    </div>
  );
}

function PreviewIllustration(): ReactNode {
  return (
    <div className="preview-illustration" aria-hidden="true">
      <img
        src="/img/preview-environments.svg"
        alt=""
        className="preview-svg"
        loading="lazy"
      />
    </div>
  );
}

export default function CloudSection(): ReactNode {
  return (
    <section className="cloud-preview-section hp-section-bordered">
      <div className="container">
        <div className="cloud-preview-grid">
          {/* Cloud card */}
          <div className="cloud-card">
            <div className="cloud-card-content">
              <h3>Laravel Cloud takes you{' '}<br className="tablet-br" />from local{' '}<br className="mobile-br" />to live in{' '}<br className="tablet-br" />seconds</h3>
              <p>
                No more guessing how many servers you{' '}<br className="tablet-br" />need: autoscale up under load
                and{' '}<br className="tablet-br" />hibernate when{' '}<br className="desktop-only-br" />idle. Only pay for what{' '}<br className="tablet-br" />you actually use.
              </p>
              <ul className="cloud-feature-list">
                <li>
                  <CheckIcon />
                  <span>Full control via dashboard or CLI</span>
                </li>
                <li>
                  <CheckIcon />
                  <span>Instantly add databases, workers,{' '}<br className="tablet-br" />cache, and storage</span>
                </li>
              </ul>
              <div className="cloud-btn-wrapper">
                <a href="https://cloud.laravel.com" className="explore-btn">
                  Explore Laravel Cloud
                  <ArrowIcon />
                </a>
              </div>
            </div>
            <div className="cloud-card-illustration">
              <AutoscaleIllustration />
            </div>
          </div>

          {/* Preview card */}
          <div className="preview-card">
            <div className="cloud-card-content">
              <h3>Check pull requests from{' '}<br className="tablet-br" />your{' '}<br className="mobile-br" />team (or agents) in{' '}<br className="tablet-br" />preview{' '}<br className="mobile-br" />environments</h3>
              <p>
                Review every change in Cloud's zero-risk,{' '}<br className="tablet-br" />production-{' '}<br className="mobile-br" />like{' '}<br className="desktop-only-br" />preview
                environment{' '}<br className="tablet-br" />before it ever hits your main{' '}<br className="mobile-br" />branch.
              </p>
              <ul className="cloud-feature-list">
                <li>
                  <CheckIcon />
                  <span>Integrates seamlessly with GitHub{' '}<br className="tablet-br" />Actions</span>
                </li>
                <li>
                  <CheckIcon />
                  <span>Test migrations and heavy changes{' '}<br className="tablet-br" />safely</span>
                </li>
              </ul>
              <div className="cloud-btn-wrapper">
                <a
                  href="https://cloud.laravel.com/docs/preview-environments"
                  className="explore-btn"
                >
                  Explore Preview Environments
                  <ArrowIcon />
                </a>
              </div>
            </div>
            <div className="cloud-card-illustration preview-card-illustration">
              <PreviewIllustration />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
