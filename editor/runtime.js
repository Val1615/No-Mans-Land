export function createStoryRuntime(doc,states={}){const messages=[];
 const status=id=>states[id]?.status||'not_started';
 function finish(id){const q=doc.quests[id],s=states[id];if(!q||!s||s.status!=='active')return false;if(!q.objectives.length||!q.objectives.every(o=>s.done.includes(o.id))){messages.push('Objectifs de quête encore incomplets.');return false;}s.status='completed';messages.push('Quête terminée : '+q.title+(q.reward?' — '+q.reward:''));return true;}
 function start(id){const q=doc.quests[id];if(!q||status(id)!=='not_started')return false;states[id]={status:'active',done:[]};messages.push('Quête commencée : '+q.title);return true;}
 function event(type,targetId){for(const q of Object.values(doc.quests)){const s=states[q.id];if(!s||s.status!=='active')continue;const pending=q.objectives.filter(o=>!s.done.includes(o.id));for(const o of q.ordered?pending.slice(0,1):pending)if(o.type===type&&o.targetId===targetId){s.done.push(o.id);messages.push('Objectif validé : '+o.text);}if(q.objectives.length&&q.objectives.every(o=>s.done.includes(o.id)))finish(q.id);}}
 function available(c){return !c.requiresQuestId||!c.requiresStatus||status(c.requiresQuestId)===c.requiresStatus;}
 function choose(c,actorId){if(!available(c))return false;if(c.action==='start')start(c.questId);if(actorId)event('talk',actorId);if(c.action==='complete')finish(c.questId);return true;}
 for(const q of Object.values(doc.quests))if(q.startMode==='automatic')start(q.id);
 return {status,start,event,choose,available,finish,states,messages,done:(q,id)=>states[q]?.done.includes(id)||false};
}
