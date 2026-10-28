/** Outline narration is separate from the player's stable scene identifiers. */
export interface OutlinePage {
  id?: string;
  title: string;
  goal?: string;
  summary?: string;
  interaction?: string;
  next?: string;
  snippet?: string;
}
export interface ModulePageOutline extends OutlinePage {id:string}
export function modulePages(pages:readonly OutlinePage[],scenes:readonly {id:string}[]=[]):ModulePageOutline[]{
  return pages.map((page,index)=>({...page,id:page.id||scenes[index]?.id||'page-'+(index+1)}));
}
