import React from 'react';
import {registerRoot, Composition, AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig} from 'remotion';

// Contoh: tajuk yang "melantun" masuk (React + Remotion).
const Tajuk = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 12}});
  return (
    <AbsoluteFill style={{background: '#0b1020', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{color: '#fff', font: '700 110px sans-serif', transform: `scale(${s})`,
        opacity: interpolate(f, [0, 15], [0, 1], {extrapolateRight: 'clamp'})}}>Ujian Remotion</div>
    </AbsoluteFill>
  );
};

registerRoot(() => (
  <Composition id="Tajuk" component={Tajuk} durationInFrames={90} fps={30} width={1920} height={1080} />
));
