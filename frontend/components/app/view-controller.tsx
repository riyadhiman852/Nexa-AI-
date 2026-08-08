'use client';
import { useState } from 'react';
import { useTheme } from 'next-themes';
import { AnimatePresence, motion } from 'motion/react';
import { useAgent, useSessionContext } from '@livekit/components-react';
import type { AppConfig } from '@/app-config';
import { AgentSessionView_01 } from '@/components/agents-ui/blocks/agent-session-view-01';
import { WelcomeView } from '@/components/app/welcome-view';
import { ConnectingView } from '@/components/app/connecting-view';
import { CallEndedView } from '@/components/app/call-ended-view';
import { NexaStatusBadge } from '@/components/app/nexa-status-badge';
const MotionWelcomeView=motion.create(WelcomeView); const MotionSessionView=motion.create(AgentSessionView_01);
const motionProps={variants:{visible:{opacity:1},hidden:{opacity:0}},initial:'hidden' as const,animate:'visible' as const,exit:'hidden' as const,transition:{duration:.35,ease:'linear' as const}};
export function ViewController({appConfig}:{appConfig:AppConfig}){
 const {isConnected,start}=useSessionContext(); const {state:agentState}=useAgent(); const {resolvedTheme}=useTheme();
 const [hasStarted,setHasStarted]=useState(false); const [micError,setMicError]=useState<string|null>(null);
 const handleStart=async()=>{setMicError(null);setHasStarted(true);try{await start();}catch{setMicError('Microphone permission is required to start a voice conversation.');}};
 const connecting=hasStarted&&!isConnected&&!micError&&['connecting','pre-connect-buffering','initializing'].includes(agentState);
 const ended=hasStarted&&!isConnected&&!micError&&!connecting&&['disconnected','failed'].includes(agentState);
 return <AnimatePresence mode="wait">
  {!hasStarted&&<MotionWelcomeView key="welcome" {...motionProps} startButtonText={appConfig.startButtonText} onStartCall={handleStart} micError={micError} onRetry={handleStart}/>}
  {hasStarted&&micError&&!isConnected&&<MotionWelcomeView key="mic-error" {...motionProps} startButtonText="Try Again" onStartCall={handleStart} micError={micError} onRetry={handleStart}/>}
  {connecting&&<motion.div key="connecting" {...motionProps}><ConnectingView/></motion.div>}
  {isConnected&&<motion.div key="session" {...motionProps} className="fixed inset-0"><NexaStatusBadge/><MotionSessionView {...motionProps} supportsChatInput={appConfig.supportsChatInput} supportsVideoInput={appConfig.supportsVideoInput} supportsScreenShare={appConfig.supportsScreenShare} isPreConnectBufferEnabled={appConfig.isPreConnectBufferEnabled} audioVisualizerType={appConfig.audioVisualizerType} audioVisualizerColor={resolvedTheme==='dark'?appConfig.audioVisualizerColorDark:appConfig.audioVisualizerColor} audioVisualizerColorShift={appConfig.audioVisualizerColorShift} audioVisualizerBarCount={appConfig.audioVisualizerBarCount} audioVisualizerGridRowCount={appConfig.audioVisualizerGridRowCount} audioVisualizerGridColumnCount={appConfig.audioVisualizerGridColumnCount} audioVisualizerRadialBarCount={appConfig.audioVisualizerRadialBarCount} audioVisualizerRadialRadius={appConfig.audioVisualizerRadialRadius} audioVisualizerWaveLineWidth={appConfig.audioVisualizerWaveLineWidth} className="fixed inset-0"/></motion.div>}
  {ended&&<motion.div key="ended" {...motionProps}><CallEndedView onStartAgain={handleStart}/></motion.div>}
 </AnimatePresence>;
}
