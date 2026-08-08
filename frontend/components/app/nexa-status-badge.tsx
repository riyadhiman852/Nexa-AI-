'use client';
import { useAgent } from '@livekit/components-react';
import { AgentChatIndicator } from '@/components/agents-ui/agent-chat-indicator';
export function NexaStatusBadge(){const {state}=useAgent();const label=state==='speaking'?'Nexa is replying':state==='thinking'?'Nexa is thinking':state==='listening'?'Nexa is listening':'Nexa is getting ready';return <div className="nexa-card absolute top-4 left-1/2 z-30 flex -translate-x-1/2 items-center gap-2 px-3 py-2 text-xs font-medium shadow-sm md:top-6">{['speaking','thinking','listening'].includes(state)?<AgentChatIndicator size="sm" className="bg-primary"/>:<span className="size-2 rounded-full bg-primary/50"/>}{label}</div>}
