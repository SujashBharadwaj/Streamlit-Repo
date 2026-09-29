"use client";

import { useState, useEffect, useRef, useCallback } from "react";

/* ─────────────────────────────────────────────
   Bijli's witty speech lines
   ───────────────────────────────────────────── */
const BIJLI_LINES = [
  "Purr… 0 compile errors detected.",
  "Sujash is building cool things. Want to see his projects?",
  "Batted at a bug. It's a feature now. 🐾",
  "⚡ Bijli is purring at optimal frequency.",
  "Meow! All services operational.",
  "I knocked your cache off the table. You're welcome.",
  "Linting your vibes… passed ✓",
  "npm install treats --save 🐟",
  "git commit -m 'fed the cat'",
  "Sujash says I'm the real 10x engineer.",
];

type Pose = "loaf" | "standing" | "curious";

/* ─────────────────────────────────────────────
   Utility: clamp & lerp
   ───────────────────────────────────────────── */
function clamp(v: number, min: number, max: number) {
  return Math.max(min, Math.min(max, v));
}
function lerp(a: number, b: number, t: number) {
  return a + (b - a) * t;
}

/* ─────────────────────────────────────────────
   Bijli — Natural Feline SVG, 3 Poses
   ───────────────────────────────────────────── */
export default function BijliCharacter() {
  /* ── State ── */
  const [isAsleep, setIsAsleep] = useState(false);
  const [speechBubble, setSpeechBubble] = useState<string | null>(null);
  const [isHovering, setIsHovering] = useState(false);
  const [pose, setPose] = useState<Pose>("loaf");

  // Smooth animated values driven by rAF
  const [eyeX, setEyeX] = useState(0);
  const [eyeY, setEyeY] = useState(0);
  const [headTilt, setHeadTilt] = useState(0);
  const [tailPhase, setTailPhase] = useState(0);
  const [blinkState, setBlinkState] = useState(1); // 1 = open, 0 = closed
  const [earTwitch, setEarTwitch] = useState(0);
  const [pawBat, setPawBat] = useState(0);

  const containerRef = useRef<HTMLDivElement>(null);
  const mouseTarget = useRef({ x: 0, y: 0 });
  const eyeCurrent = useRef({ x: 0, y: 0 });
  const headCurrent = useRef(0);
  const speechTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);
  const lastLineIdx = useRef(-1);
  const rafRef = useRef<number>(0);

  /* ── Pose cycling ── */
  useEffect(() => {
    if (isAsleep) return;
    const interval = setInterval(() => {
      setPose((prev) => {
        const poses: Pose[] = ["loaf", "standing", "curious"];
        const others = poses.filter((p) => p !== prev);
        return others[Math.floor(Math.random() * others.length)];
      });
    }, 14000 + Math.random() * 8000);
    return () => clearInterval(interval);
  }, [isAsleep]);

  /* ── Mouse tracking (target) ── */
  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (isAsleep || !containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = e.clientX - cx;
      const dy = e.clientY - cy;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;

      mouseTarget.current = {
        x: clamp((dx / dist) * Math.min(dist * 0.012, 4), -4, 4),
        y: clamp((dy / dist) * Math.min(dist * 0.012, 3), -3, 3),
      };
    },
    [isAsleep]
  );

  useEffect(() => {
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [handleMouseMove]);

  /* ── Animation loop ── */
  useEffect(() => {
    let lastTime = 0;
    let blinkTimer = 3000 + Math.random() * 3000;
    let earTimer = 5000 + Math.random() * 4000;

    const animate = (time: number) => {
      const dt = lastTime ? (time - lastTime) / 1000 : 0.016;
      lastTime = time;

      if (!isAsleep) {
        // Smooth eye follow
        eyeCurrent.current.x = lerp(eyeCurrent.current.x, mouseTarget.current.x, 0.08);
        eyeCurrent.current.y = lerp(eyeCurrent.current.y, mouseTarget.current.y, 0.08);
        setEyeX(eyeCurrent.current.x);
        setEyeY(eyeCurrent.current.y);

        // Head tilt toward cursor
        const targetTilt = clamp(mouseTarget.current.x * 2, -8, 8);
        headCurrent.current = lerp(headCurrent.current, targetTilt, 0.05);
        setHeadTilt(headCurrent.current);

        // Blink timer
        blinkTimer -= dt * 1000;
        if (blinkTimer <= 0) {
          setBlinkState(0);
          setTimeout(() => setBlinkState(1), 120);
          if (Math.random() < 0.3) {
            setTimeout(() => setBlinkState(0), 300);
            setTimeout(() => setBlinkState(1), 420);
          }
          blinkTimer = 3000 + Math.random() * 4000;
        }

        // Ear twitch timer
        earTimer -= dt * 1000;
        if (earTimer <= 0) {
          setEarTwitch(1);
          setTimeout(() => setEarTwitch(0), 200);
          earTimer = 5000 + Math.random() * 6000;
        }
      }

      // Tail sway (always active, slower when sleeping)
      setTailPhase((p) => p + dt * (isAsleep ? 0.8 : 1.6));

      rafRef.current = requestAnimationFrame(animate);
    };

    rafRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(rafRef.current);
  }, [isAsleep]);

  /* ── Click → speech bubble + paw bat ── */
  const handleClick = () => {
    if (isAsleep) {
      setIsAsleep(false);
      return;
    }

    // Trigger paw bat animation
    setPawBat(1);
    setTimeout(() => setPawBat(0), 400);

    // Cycle pose on click
    setPose((prev) => {
      const poses: Pose[] = ["loaf", "standing", "curious"];
      const idx = poses.indexOf(prev);
      return poses[(idx + 1) % poses.length];
    });

    // Speech bubble
    let idx: number;
    do {
      idx = Math.floor(Math.random() * BIJLI_LINES.length);
    } while (idx === lastLineIdx.current && BIJLI_LINES.length > 1);
    lastLineIdx.current = idx;

    setSpeechBubble(BIJLI_LINES[idx]);
    if (speechTimeout.current) clearTimeout(speechTimeout.current);
    speechTimeout.current = setTimeout(() => setSpeechBubble(null), 3500);
  };

  /* ── Cleanup ── */
  useEffect(() => {
    return () => {
      if (speechTimeout.current) clearTimeout(speechTimeout.current);
    };
  }, []);

  /* ── Computed SVG values ── */
  const tailSwing = Math.sin(tailPhase) * (isAsleep ? 4 : 10);
  const tailSwing2 = Math.sin(tailPhase * 1.3 + 0.5) * (isAsleep ? 2 : 6);
  const breatheScale = isAsleep
    ? 1 + Math.sin(tailPhase * 0.5) * 0.008
    : 1 + Math.sin(tailPhase * 0.8) * 0.012;
  const earTwitchOffset = earTwitch * 3;
  const pawBatAngle = pawBat * -25;

  /* ─────────────────────────────────────────────
     SVG Sub-components: Shared parts
     ───────────────────────────────────────────── */

  /* ── Natural feline head ── */
  const renderHead = (cx: number, cy: number) => (
    <g transform={`rotate(${headTilt}, ${cx}, ${cy + 12})`}>
      {/* Head shape — natural cat skull, slightly triangular */}
      <path
        d={`M ${cx - 28},${cy + 8} 
            Q ${cx - 32},${cy - 8} ${cx - 20},${cy - 18} 
            Q ${cx - 8},${cy - 28} ${cx},${cy - 26}
            Q ${cx + 8},${cy - 28} ${cx + 20},${cy - 18}
            Q ${cx + 32},${cy - 8} ${cx + 28},${cy + 8}
            Q ${cx + 24},${cy + 18} ${cx},${cy + 20}
            Q ${cx - 24},${cy + 18} ${cx - 28},${cy + 8} Z`}
        fill="#1a1a1e"
        filter="url(#fur-shadow)"
      />
      {/* Cheek fluff — left */}
      <ellipse cx={cx - 20} cy={cy + 6} rx={10} ry={8} fill="#1e1e22" />
      {/* Cheek fluff — right */}
      <ellipse cx={cx + 20} cy={cy + 6} rx={10} ry={8} fill="#1e1e22" />

      {/* ── EARS — tall, upright, alert, pointed ── */}
      {/* Left ear — tall triangle angled slightly outward */}
      <path
        d={`M ${cx - 18},${cy - 14}
            L ${cx - 28 - earTwitchOffset},${cy - 50 - earTwitchOffset}
            L ${cx - 6},${cy - 18} Z`}
        fill="#1a1a1e"
      />
      {/* Left ear inner pink */}
      <path
        d={`M ${cx - 16},${cy - 16}
            L ${cx - 26 - earTwitchOffset * 0.7},${cy - 44 - earTwitchOffset * 0.7}
            L ${cx - 8},${cy - 19} Z`}
        fill="#3d2828"
      />
      {/* Right ear — tall triangle angled slightly outward */}
      <path
        d={`M ${cx + 18},${cy - 14}
            L ${cx + 28 + earTwitchOffset},${cy - 50 - earTwitchOffset}
            L ${cx + 6},${cy - 18} Z`}
        fill="#1a1a1e"
      />
      {/* Right ear inner pink */}
      <path
        d={`M ${cx + 16},${cy - 16}
            L ${cx + 26 + earTwitchOffset * 0.7},${cy - 44 - earTwitchOffset * 0.7}
            L ${cx + 8},${cy - 19} Z`}
        fill="#3d2828"
      />

      {/* ── EYES — natural almond feline shape ── */}
      {isAsleep ? (
        <>
          <path d={`M ${cx - 18},${cy - 2} Q ${cx - 12},${cy + 3} ${cx - 6},${cy - 2}`} fill="none" stroke="#555" strokeWidth="2" strokeLinecap="round" />
          <path d={`M ${cx + 6},${cy - 2} Q ${cx + 12},${cy + 3} ${cx + 18},${cy - 2}`} fill="none" stroke="#555" strokeWidth="2" strokeLinecap="round" />
        </>
      ) : (
        <>
          {/* Eye sockets — almond shaped */}
          <ellipse cx={cx - 12} cy={cy - 1} rx={8} ry={6.5 * blinkState} fill="#0d0d0f" />
          <ellipse cx={cx + 12} cy={cy - 1} rx={8} ry={6.5 * blinkState} fill="#0d0d0f" />
          {blinkState > 0.5 && (
            <>
              {/* Iris — amber gold glow */}
              <ellipse cx={cx - 12 + eyeX} cy={cy - 1 + eyeY} rx={5.5} ry={5.5} fill="url(#eye-glow)" />
              <ellipse cx={cx + 12 + eyeX} cy={cy - 1 + eyeY} rx={5.5} ry={5.5} fill="url(#eye-glow)" />
              {/* Vertical slit pupils */}
              <ellipse cx={cx - 12 + eyeX} cy={cy - 1 + eyeY} rx={1.8} ry={4.5} fill="#111" />
              <ellipse cx={cx + 12 + eyeX} cy={cy - 1 + eyeY} rx={1.8} ry={4.5} fill="#111" />
              {/* Eye shine highlights */}
              <circle cx={cx - 14 + eyeX * 0.5} cy={cy - 3.5 + eyeY * 0.5} r={1.5} fill="rgba(255,255,255,0.65)" />
              <circle cx={cx + 10 + eyeX * 0.5} cy={cy - 3.5 + eyeY * 0.5} r={1.5} fill="rgba(255,255,255,0.65)" />
              {/* Small secondary highlight */}
              <circle cx={cx - 10 + eyeX * 0.3} cy={cy + 1 + eyeY * 0.3} r={0.8} fill="rgba(255,255,255,0.3)" />
              <circle cx={cx + 14 + eyeX * 0.3} cy={cy + 1 + eyeY * 0.3} r={0.8} fill="rgba(255,255,255,0.3)" />
            </>
          )}
        </>
      )}

      {/* ── NOSE — small inverted triangle with natural shape ── */}
      <path
        d={`M ${cx},${cy + 8} L ${cx - 3},${cy + 11} Q ${cx},${cy + 12.5} ${cx + 3},${cy + 11} Z`}
        fill="#6b4444"
      />

      {/* ── MOUTH — natural cat W-shape ── */}
      <path
        d={`M ${cx - 5},${cy + 12.5} Q ${cx - 2},${cy + 15} ${cx},${cy + 13} Q ${cx + 2},${cy + 15} ${cx + 5},${cy + 12.5}`}
        fill="none" stroke="#3a2a2a" strokeWidth="1" strokeLinecap="round"
      />

      {/* ── WHISKERS — natural radiating sets ── */}
      {/* Left whiskers */}
      <line x1={cx - 18} y1={cy + 5} x2={cx - 42} y2={cy + 1} stroke="#555" strokeWidth="0.7" opacity="0.5" />
      <line x1={cx - 18} y1={cy + 8} x2={cx - 43} y2={cy + 8} stroke="#555" strokeWidth="0.7" opacity="0.5" />
      <line x1={cx - 17} y1={cy + 11} x2={cx - 40} y2={cy + 15} stroke="#555" strokeWidth="0.7" opacity="0.5" />
      {/* Right whiskers */}
      <line x1={cx + 18} y1={cy + 5} x2={cx + 42} y2={cy + 1} stroke="#555" strokeWidth="0.7" opacity="0.5" />
      <line x1={cx + 18} y1={cy + 8} x2={cx + 43} y2={cy + 8} stroke="#555" strokeWidth="0.7" opacity="0.5" />
      <line x1={cx + 17} y1={cy + 11} x2={cx + 40} y2={cy + 15} stroke="#555" strokeWidth="0.7" opacity="0.5" />

      {/* ── Whisker dots (follicle bumps) ── */}
      <circle cx={cx - 8} cy={cy + 9} r="0.8" fill="#444" />
      <circle cx={cx - 7} cy={cy + 11} r="0.8" fill="#444" />
      <circle cx={cx + 8} cy={cy + 9} r="0.8" fill="#444" />
      <circle cx={cx + 7} cy={cy + 11} r="0.8" fill="#444" />
    </g>
  );

  /* ── Red collar with bell ── */
  const renderCollar = (cx: number, cy: number, rx: number) => (
    <g>
      <ellipse cx={cx} cy={cy} rx={rx} ry={5} fill="#cc2233" />
      <ellipse cx={cx} cy={cy} rx={rx} ry={4} fill="#aa1a28" />
      <ellipse cx={cx} cy={cy} rx={rx - 2} ry={3.5} fill="none" stroke="#dd3344" strokeWidth="0.5" strokeDasharray="3,3" />
      {/* Golden lightning bolt charm */}
      <g transform={`translate(${cx},${cy + 6})`}>
        <polygon points="0,-5 2,-1 -1,-1.5 0,5 -2,1 1,1.5" fill="#FFD700" />
        <circle cx="0" cy="-6" r="1.5" fill="#DAA520" />
      </g>
    </g>
  );

  /* ─────────────────────────────────────────────
     POSE RENDERERS
     ───────────────────────────────────────────── */

  /* ── LOAF POSE: compact blob, paws tucked, tail wrapped ── */
  const renderLoaf = () => (
    <g transform={`translate(100,105) scale(${breatheScale}) translate(-100,-105)`}>
      {/* Tail behind body — curled around side */}
      <path
        d={`M 55,138 Q ${40 + tailSwing * 0.6},${148 + tailSwing2 * 0.5} ${32 + tailSwing * 0.8},${135} 
            Q ${28 + tailSwing},${122} ${35},${115}`}
        fill="none" stroke="#1a1a1e" strokeWidth="10" strokeLinecap="round"
      />
      {/* Tail fluff tip */}
      <circle cx={35} cy={115} r="6" fill="#1a1a1e" />

      {/* Main body — compact loaf oval */}
      <ellipse cx="100" cy="140" rx="46" ry="28" fill="#1a1a1e" filter="url(#fur-shadow)" />
      {/* Belly fluff */}
      <ellipse cx="100" cy="144" rx="30" ry="16" fill="#222226" />
      {/* Fur tufts on sides */}
      <ellipse cx="62" cy="136" rx="10" ry="16" fill="#1e1e22" />
      <ellipse cx="138" cy="136" rx="10" ry="16" fill="#1e1e22" />

      {/* Front — tucked paws just peeking */}
      <ellipse cx="80" cy="158" rx="8" ry="5" fill="#1a1a1e" />
      <ellipse cx="120" cy="158" rx="8" ry="5" fill="#1a1a1e" />
      {/* Tiny paw pads */}
      <circle cx="78" cy="159" r="1.5" fill="#3a3a3e" />
      <circle cx="82" cy="159" r="1.5" fill="#3a3a3e" />
      <circle cx="118" cy="159" r="1.5" fill="#3a3a3e" />
      <circle cx="122" cy="159" r="1.5" fill="#3a3a3e" />

      {/* Collar */}
      {renderCollar(100, 124, 30)}

      {/* Head */}
      {renderHead(100, 102)}
    </g>
  );

  /* ── STANDING POSE: four legs visible, arched back, tail high ── */
  const renderStanding = () => (
    <g transform={`translate(100,105) scale(${breatheScale}) translate(-100,-105)`}>
      {/* Tail — held high behind with expressive curve */}
      <path
        d={`M 50,120 Q ${35 + tailSwing},${100 + tailSwing2} ${30 + tailSwing * 1.2},${80}
            Q ${28 + tailSwing * 1.4},${65} ${35 + tailSwing * 0.6},${55}`}
        fill="none" stroke="#1a1a1e" strokeWidth="10" strokeLinecap="round"
      />
      <circle cx={35 + tailSwing * 0.6} cy={55} r="6" fill="#1a1a1e" />

      {/* Body — elongated horizontal shape */}
      <ellipse cx="95" cy="128" rx="50" ry="22" fill="#1a1a1e" filter="url(#fur-shadow)" />
      {/* Chest fluff */}
      <ellipse cx="110" cy="130" rx="20" ry="14" fill="#222226" />
      {/* Back arch */}
      <path
        d="M 55,118 Q 75,105 100,108 Q 125,105 140,118"
        fill="#1a1a1e" stroke="#1a1a1e" strokeWidth="6"
      />
      {/* Fur texture lines */}
      <ellipse cx="70" cy="124" rx="8" ry="14" fill="#1e1e22" />
      <ellipse cx="125" cy="124" rx="8" ry="14" fill="#1e1e22" />

      {/* ── FOUR LEGS — short, stubby, fluffy ── */}
      {/* Back left leg */}
      <path d="M 62,140 L 58,164 Q 56,170 62,170 L 70,170 Q 74,170 72,164 L 68,142" fill="#1a1a1e" />
      <ellipse cx="66" cy="170" rx="7" ry="4" fill="#1a1a1e" />
      <circle cx="63" cy="171" r="1.5" fill="#3a3a3e" />
      <circle cx="66" cy="172" r="1.5" fill="#3a3a3e" />
      <circle cx="69" cy="171" r="1.5" fill="#3a3a3e" />

      {/* Back right leg */}
      <path d="M 78,141 L 76,164 Q 74,170 80,170 L 88,170 Q 92,170 90,164 L 86,142" fill="#1a1a1e" />
      <ellipse cx="84" cy="170" rx="7" ry="4" fill="#1a1a1e" />
      <circle cx="81" cy="171" r="1.5" fill="#3a3a3e" />
      <circle cx="84" cy="172" r="1.5" fill="#3a3a3e" />
      <circle cx="87" cy="171" r="1.5" fill="#3a3a3e" />

      {/* Front left leg (with paw bat) */}
      <g transform={`rotate(${pawBatAngle}, 115, 140)`}>
        <path d="M 112,138 L 110,162 Q 108,168 114,168 L 122,168 Q 126,168 124,162 L 120,140" fill="#1a1a1e" />
        <ellipse cx="118" cy="168" rx="7" ry="4" fill="#1a1a1e" />
        <circle cx="115" cy="169" r="1.5" fill="#3a3a3e" />
        <circle cx="118" cy="170" r="1.5" fill="#3a3a3e" />
        <circle cx="121" cy="169" r="1.5" fill="#3a3a3e" />
      </g>

      {/* Front right leg */}
      <path d="M 130,137 L 128,162 Q 126,168 132,168 L 140,168 Q 144,168 142,162 L 138,138" fill="#1a1a1e" />
      <ellipse cx="136" cy="168" rx="7" ry="4" fill="#1a1a1e" />
      <circle cx="133" cy="169" r="1.5" fill="#3a3a3e" />
      <circle cx="136" cy="170" r="1.5" fill="#3a3a3e" />
      <circle cx="139" cy="169" r="1.5" fill="#3a3a3e" />

      {/* Collar */}
      {renderCollar(120, 118, 24)}

      {/* Head — positioned at front */}
      {renderHead(128, 96)}
    </g>
  );

  /* ── CURIOUS POSE: sitting upright on hindlegs, paws raised ── */
  const renderCurious = () => (
    <g transform={`translate(100,105) scale(${breatheScale}) translate(-100,-105)`}>
      {/* Tail — curled at base, resting behind */}
      <path
        d={`M 70,160 Q ${55 + tailSwing * 0.5},${168 + tailSwing2 * 0.4} ${42 + tailSwing * 0.7},${158}
            Q ${35 + tailSwing},${148} ${40},${140}`}
        fill="none" stroke="#1a1a1e" strokeWidth="10" strokeLinecap="round"
      />
      <circle cx={40} cy={140} r="6" fill="#1a1a1e" />

      {/* Haunches / lower body — sitting base */}
      <ellipse cx="100" cy="155" rx="34" ry="22" fill="#1a1a1e" filter="url(#fur-shadow)" />
      {/* Hind paws visible at base */}
      <ellipse cx="78" cy="172" rx="10" ry="5" fill="#1a1a1e" />
      <ellipse cx="122" cy="172" rx="10" ry="5" fill="#1a1a1e" />
      <circle cx="75" cy="173" r="1.5" fill="#3a3a3e" />
      <circle cx="78" cy="174" r="1.5" fill="#3a3a3e" />
      <circle cx="81" cy="173" r="1.5" fill="#3a3a3e" />
      <circle cx="119" cy="173" r="1.5" fill="#3a3a3e" />
      <circle cx="122" cy="174" r="1.5" fill="#3a3a3e" />
      <circle cx="125" cy="173" r="1.5" fill="#3a3a3e" />

      {/* Upright torso — tall oval */}
      <ellipse cx="100" cy="128" rx="28" ry="34" fill="#1a1a1e" filter="url(#fur-shadow)" />
      {/* Chest fluff — lighter patch */}
      <ellipse cx="100" cy="132" rx="18" ry="20" fill="#252528" />
      {/* Fur tuft center */}
      <path d="M 94,118 Q 97,112 100,118 Q 103,112 106,118" fill="#2a2a2e" stroke="#2a2a2e" strokeWidth="0.5" />

      {/* ── FRONT PAWS — raised daintily near chest ── */}
      <g transform={`rotate(${pawBatAngle * 0.5}, 85, 132)`}>
        <path d="M 78,130 Q 72,136 74,142 Q 76,146 82,144 L 84,134" fill="#1a1a1e" />
        <ellipse cx="78" cy="144" rx="5" ry="3.5" fill="#1a1a1e" />
        <circle cx="76" cy="145" r="1.2" fill="#3a3a3e" />
        <circle cx="79" cy="145.5" r="1.2" fill="#3a3a3e" />
      </g>
      <g>
        <path d="M 122,130 Q 128,136 126,142 Q 124,146 118,144 L 116,134" fill="#1a1a1e" />
        <ellipse cx="122" cy="144" rx="5" ry="3.5" fill="#1a1a1e" />
        <circle cx="120" cy="145" r="1.2" fill="#3a3a3e" />
        <circle cx="123" cy="145.5" r="1.2" fill="#3a3a3e" />
      </g>

      {/* Collar */}
      {renderCollar(100, 108, 22)}

      {/* Head — sitting high */}
      {renderHead(100, 82)}
    </g>
  );

  return (
    <div className="bijli-wrapper" ref={containerRef}>
      {/* Speech bubble — anchored LEFT */}
      {speechBubble && (
        <div className="bijli-speech" key={speechBubble}>
          <span>{speechBubble}</span>
        </div>
      )}

      {/* SVG Cat */}
      <div
        className={`bijli-card ${isAsleep ? "bijli-sleeping" : ""} ${isHovering ? "bijli-alert" : ""}`}
        onClick={handleClick}
        onMouseEnter={() => setIsHovering(true)}
        onMouseLeave={() => setIsHovering(false)}
        role="button"
        tabIndex={0}
        aria-label="Click to interact with Bijli the cat"
        onKeyDown={(e) => e.key === "Enter" && handleClick()}
      >
        <svg
          viewBox="0 0 200 200"
          width="200"
          height="200"
          xmlns="http://www.w3.org/2000/svg"
          style={{ overflow: "visible" }}
        >
          {/* ── Defs ── */}
          <defs>
            <radialGradient id="bijli-glow" cx="50%" cy="60%" r="45%">
              <stop offset="0%" stopColor="#20A4F3" stopOpacity="0.06" />
              <stop offset="100%" stopColor="#011627" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="eye-glow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FFD700" stopOpacity="0.9" />
              <stop offset="60%" stopColor="#CC8800" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#996600" stopOpacity="0" />
            </radialGradient>
            <filter id="fur-shadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#000" floodOpacity="0.4" />
            </filter>
          </defs>

          <circle cx="100" cy="100" r="95" fill="url(#bijli-glow)" />

          {/* ── Render active pose ── */}
          {pose === "loaf" && renderLoaf()}
          {pose === "standing" && renderStanding()}
          {pose === "curious" && renderCurious()}

          {/* ── Sleeping ZZZ ── */}
          {isAsleep && (
            <g>
              <text x="140" y="65" fontSize="16" fill="#20A4F3" opacity="0.6"
                style={{ animation: "bijli-zzz-float 2s ease-in-out infinite" }}>z</text>
              <text x="152" y="52" fontSize="13" fill="#20A4F3" opacity="0.4"
                style={{ animation: "bijli-zzz-float 2s ease-in-out infinite 0.4s" }}>z</text>
              <text x="160" y="40" fontSize="10" fill="#20A4F3" opacity="0.3"
                style={{ animation: "bijli-zzz-float 2s ease-in-out infinite 0.8s" }}>z</text>
            </g>
          )}
        </svg>
      </div>

      {/* Status badge & sleep toggle — uses native site styling */}
      <div className="bijli-status-row">
        <span className="bijli-badge">
          <span className={`bijli-dot ${isAsleep ? "bijli-dot-sleep" : ""}`} />
          ⚡ Bijli • {isAsleep ? "Napping" : "Chief Morale Familiar"}
        </span>
        <button
          className="bijli-toggle"
          onClick={() => {
            setIsAsleep((s) => !s);
            setSpeechBubble(null);
          }}
          title={isAsleep ? "Wake Bijli up" : "Let Bijli nap"}
        >
          {isAsleep ? "☀️" : "🌙"}
        </button>
      </div>
    </div>
  );
}
