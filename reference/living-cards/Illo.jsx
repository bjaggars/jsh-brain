// Looping card illustrations — bundled SVG, animated like a gif, still under reduced motion.
const S = { fill: 'none', stroke: 'var(--ink)', strokeWidth: 2, strokeLinecap: 'round', strokeLinejoin: 'round' };
const B = 'var(--blue)';
const A = 'var(--amber)';

const ART = {
  business_context: (
    <g>
      <path {...S} d="M28 34h64v34H28z" />
      <path {...S} d="M24 34l8-14h56l8 14" />
      <path {...S} d="M54 68V50h12v18" />
      <g className="a-swing" style={{ transformOrigin: '60px 20px' }}>
        <path {...S} d="M60 20v6" />
        <rect x="46" y="26" width="28" height="8" rx="2" fill={B} />
      </g>
      <rect x="34" y="42" width="12" height="10" fill={A} className="a-blink" />
    </g>
  ),
  landscape: (
    <g>
      <rect x="18" y="18" width="30" height="24" rx="3" {...S} className="a-slide-r" />
      <rect x="72" y="18" width="30" height="24" rx="3" {...S} className="a-slide-l" />
      <rect x="45" y="44" width="30" height="24" rx="3" fill={B} className="a-pulse" />
      <path d="M50 52h20M50 58h14" stroke="var(--sheet)" strokeWidth="2" strokeLinecap="round" />
    </g>
  ),
  personas: (
    <g>
      {[30, 60, 90].map((x, i) => (
        <g key={x} className="a-bob" style={{ animationDelay: `${i * 0.25}s` }}>
          <circle cx={x} cy="32" r="8" fill={i === 1 ? B : 'none'} {...(i === 1 ? {} : S)} />
          <path {...S} d={`M${x - 13} 64c0-10 6-17 13-17s13 7 13 17`} />
        </g>
      ))}
    </g>
  ),
  journeys: (
    <g>
      <path d="M16 60c16-30 30 10 46-14s28-20 42-26" {...S} strokeDasharray="3 6" />
      <circle r="6" fill={A} className="a-travel" style={{ offsetPath: "path('M16 60c16-30 30 10 46-14s28-20 42-26')" }} />
      <circle cx="104" cy="20" r="4" fill={B} />
    </g>
  ),
  data_objects: (
    <g>
      {[52, 38, 24].map((y, i) => (
        <g key={y}>
          <path {...S} d={`M36 ${y}v10c0 4 11 7 24 7s24-3 24-7v-10`} />
          <ellipse cx="60" cy={y} rx="24" ry="7" {...S} fill={i === 2 ? B : 'none'} className={i === 2 ? 'a-pulse' : ''} />
        </g>
      ))}
    </g>
  ),
  screens: (
    <g>
      <rect x="16" y="16" width="62" height="42" rx="3" {...S} />
      <path {...S} d="M38 66h18M47 58v8" />
      <rect x="84" y="24" width="22" height="42" rx="4" {...S} />
      <g className="a-scroll">
        <path d="M24 26h40M24 34h28M24 42h36M24 50h22" stroke={B} strokeWidth="3" strokeLinecap="round" />
      </g>
      <rect x="88" y="32" width="14" height="6" rx="1" fill={A} className="a-blink" />
    </g>
  ),
  integrations: (
    <g>
      <circle cx="26" cy="40" r="12" {...S} />
      <circle cx="94" cy="40" r="12" {...S} />
      <path {...S} d="M38 40h44" strokeDasharray="4 5" />
      <circle r="5" fill={B} className="a-shuttle" style={{ offsetPath: "path('M38 40H82')" }} />
      <circle cx="26" cy="40" r="4" fill={A} />
      <circle cx="94" cy="40" r="4" fill={A} />
    </g>
  ),
  roles_permissions: (
    <g>
      <rect x="40" y="38" width="40" height="30" rx="4" fill={B} />
      <g className="a-unlock" style={{ transformOrigin: '72px 38px' }}>
        <path {...S} d="M48 38V28a12 12 0 0 1 24 0v10" />
      </g>
      <circle cx="60" cy="51" r="4" fill="var(--sheet)" />
      <path d="M60 54v6" stroke="var(--sheet)" strokeWidth="3" strokeLinecap="round" />
    </g>
  ),
  non_functionals: (
    <g>
      <path {...S} d="M22 62a38 38 0 0 1 76 0" />
      <path d="M30 62a30 30 0 0 1 12-24" stroke={A} strokeWidth="4" fill="none" strokeLinecap="round" />
      <g className="a-needle" style={{ transformOrigin: '60px 62px' }}>
        <path d="M60 62L60 32" stroke={B} strokeWidth="3" strokeLinecap="round" />
      </g>
      <circle cx="60" cy="62" r="4" fill="var(--ink)" />
    </g>
  ),
  design_tokens: (
    <g>
      <path {...S} d="M60 16c-24 0-40 16-40 32 0 10 8 16 18 16 6 0 8-4 8-8s4-8 10-8h14c12 0 22-8 22-16 0-10-14-16-32-16z" />
      {[[40, 36], [56, 26], [74, 28], [86, 40]].map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r="5" className="a-swatch" style={{ animationDelay: `${i * 0.4}s` }} />
      ))}
    </g>
  ),
  voices: (
    <g>
      <g className="a-talk">
        <path {...S} d="M18 22h46v24H34l-10 8v-8h-6z" fill={B} stroke={B} />
      </g>
      <g className="a-talk" style={{ animationDelay: '0.9s' }}>
        <path {...S} d="M56 38h46v24h-6v8l-10-8H56z" />
      </g>
    </g>
  ),
  questions: (
    <g>
      <path {...S} d="M24 18h72v36H56l-14 12V54H24z" />
      {[46, 60, 74].map((x, i) => (
        <circle key={x} cx={x} cy="36" r="4" fill={B} className="a-dot" style={{ animationDelay: `${i * 0.2}s` }} />
      ))}
    </g>
  ),
  assumptions: (
    <g>
      <path {...S} d="M36 70V14" />
      <g className="a-wave" style={{ transformOrigin: '36px 16px' }}>
        <path d="M36 16c14-6 24 6 44 0v26c-20 6-30-6-44 0z" fill={A} />
      </g>
    </g>
  ),
  decisions: (
    <g>
      <circle cx="60" cy="32" r="18" fill={A} className="a-glow" />
      <path {...S} d="M52 52h16M54 60h12M60 20v-6M42 32h-6M84 32h-6" />
      <path d="M54 34l5 5 8-10" stroke="var(--ink)" strokeWidth="2.5" fill="none" strokeLinecap="round" />
    </g>
  ),
  apps: (
    <g>
      {[0, 1, 2].flatMap((r) => [0, 1, 2].map((c) => (
        <rect key={`${r}${c}`} x={34 + c * 18} y={12 + r * 20} width="14" height="14" rx="3"
          fill={(r + c) % 3 === 0 ? B : 'none'} {...((r + c) % 3 === 0 ? {} : S)}
          className="a-pop" style={{ animationDelay: `${(r * 3 + c) * 0.12}s` }} />
      )))}
    </g>
  ),
  wishes: (
    <g>
      <path className="a-twinkle" style={{ transformOrigin: '60px 38px' }} fill={A}
        d="M60 14l6 16 17 1-13 11 5 17-15-9-15 9 5-17-13-11 17-1z" />
      <circle cx="28" cy="22" r="3" fill={B} className="a-blink" />
      <circle cx="94" cy="58" r="3" fill={B} className="a-blink" style={{ animationDelay: '0.7s' }} />
    </g>
  ),
};

export default function Illo({ kind }) {
  return (
    <svg className="illo" viewBox="0 0 120 80" role="img" aria-hidden="true">
      {ART[kind] || null}
    </svg>
  );
}
