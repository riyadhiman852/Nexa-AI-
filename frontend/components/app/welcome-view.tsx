'use client';
import { motion } from 'motion/react';
import { GlobeIcon, MicrophoneIcon, SparkleIcon } from '@phosphor-icons/react';
import { Button } from '@/components/ui/button';
interface WelcomeViewProps { startButtonText:string; onStartCall:()=>void; micError?:string|null; onRetry?:()=>void; }
export const WelcomeView = ({startButtonText,onStartCall,micError,onRetry,ref}:React.ComponentProps<'div'>&WelcomeViewProps)=>(
<div ref={ref} className="relative flex min-h-svh w-full items-center justify-center overflow-hidden px-5 py-10">
 <div className="nexa-blob nexa-blob-a"/><div className="nexa-blob nexa-blob-b"/>
 <main className="relative z-10 flex w-full max-w-2xl flex-col items-center text-center">
  <motion.div initial={{opacity:0,y:10}} animate={{opacity:1,y:0}} className="mb-7 flex items-center gap-3">
   <img src="/nexa-logo.svg" alt="" className="size-11 dark:hidden"/><img src="/nexa-logo-dark.svg" alt="" className="hidden size-11 dark:block"/>
   <span className="text-2xl font-semibold tracking-tight">Nexa AI</span>
  </motion.div>
  <motion.div initial={{opacity:0,scale:.97}} animate={{opacity:1,scale:1}} className="nexa-card w-full max-w-xl px-6 py-9 sm:px-10 sm:py-12">
   <div className="mx-auto mb-6 flex size-16 items-center justify-center rounded-2xl bg-primary/10 text-primary"><MicrophoneIcon size={32} weight="duotone"/></div>
   <div className="mb-3 inline-flex items-center gap-1.5 rounded-full border border-primary/15 bg-primary/5 px-3 py-1 text-xs font-medium text-primary"><SparkleIcon size={14} weight="fill"/> Voice AI for learning</div>
   <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Your AI Voice Study Companion</h1>
   <p className="text-muted-foreground mx-auto mt-4 max-w-lg text-sm leading-6 sm:text-base">Ask questions, learn programming, explore AI, plan your studies, and get friendly academic guidance through voice.</p>
   <div className="mt-6 flex flex-wrap justify-center gap-2">
    <span className="nexa-chip"><GlobeIcon size={14}/> English</span><span className="nexa-chip">हिंदी</span><span className="nexa-chip">Hinglish</span>
   </div>
   {micError&&<div className="mt-6 rounded-2xl border border-destructive/20 bg-destructive/5 p-4 text-left"><p className="font-medium text-destructive">Microphone access is blocked</p><p className="text-muted-foreground mt-1 text-sm leading-5">Allow microphone access for this site in your browser settings, then try again.</p>{onRetry&&<Button variant="outline" size="sm" onClick={onRetry} className="mt-3">Try Again</Button>}</div>}
   <Button size="lg" onClick={onStartCall} className="mt-7 h-12 w-full rounded-full font-semibold shadow-sm sm:w-72"><MicrophoneIcon size={19} weight="bold"/>{startButtonText}</Button>
   <p className="text-muted-foreground mt-4 text-xs">Voice AI • Ready to help</p>
  </motion.div>
  <p className="text-muted-foreground mt-6 text-xs">Built for students • Learn in the language that feels natural to you</p>
 </main>
</div>);
