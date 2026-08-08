export interface AppConfig {
  pageTitle: string; pageDescription: string; companyName: string;
  supportsChatInput: boolean; supportsVideoInput: boolean; supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean; logo: string; startButtonText: string;
  accent?: string; logoDark?: string; accentDark?: string;
  audioVisualizerType?: 'bar' | 'wave' | 'grid' | 'radial' | 'aura';
  audioVisualizerColor?: `#${string}`; audioVisualizerColorDark?: `#${string}`;
  audioVisualizerColorShift?: number; audioVisualizerBarCount?: number;
  audioVisualizerGridRowCount?: number; audioVisualizerGridColumnCount?: number;
  audioVisualizerRadialBarCount?: number; audioVisualizerRadialRadius?: number;
  audioVisualizerWaveLineWidth?: number; agentName?: string; sandboxId?: string;
}
export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Nexa AI',
  pageTitle: 'Nexa AI — Your AI Voice Study Companion',
  pageDescription: 'Ask questions, learn programming, explore AI, plan your studies, and get friendly academic guidance through voice.',
  supportsChatInput: true, supportsVideoInput: true, supportsScreenShare: true,
  isPreConnectBufferEnabled: true, logo: '/nexa-logo.svg', accent: '#4F46E5',
  logoDark: '/nexa-logo-dark.svg', accentDark: '#818CF8', startButtonText: 'Start Conversation',
  audioVisualizerType: 'bar', audioVisualizerColor: '#4F46E5', audioVisualizerColorDark: '#818CF8',
  audioVisualizerColorShift: 0.3, audioVisualizerBarCount: 5,
  agentName: process.env.AGENT_NAME ?? undefined, sandboxId: undefined,
};
