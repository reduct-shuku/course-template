import { ModuleShell } from '@shared/react';
import { SceneDeck, type DeckDefinition } from '@shared/react/presentation';
import { UiKitPage } from '@shared/react/routing/UiKitPage';
import { activeModules } from './modules';
import type { AppRoute } from './Router';
import { HomePage } from './HomePage';

const pptModules = activeModules.filter((module) => module.pptDeck);
const pptCatalog = pptModules.map((module) => module.pptDeck) as [DeckDefinition, ...DeckDefinition[]];

function SceneDeckPage() {
  if (!pptCatalog.length) return <ModuleShell title="SceneDeck" subtitle="暂无课程。添加带有 PPT 入口的模块后，将自动出现在这里。" />;
  return <SceneDeck
    catalog={pptCatalog}
    moduleId={(deckId) => deckId}
    assetId={(deckId) => pptModules.find((module) => module.pptDeck?.id === deckId)?.assetId ?? deckId}
    progressKey={(deckId) => `lesson-flow:${deckId}`}
    getNotes={(sceneId, deckId) => pptModules.find((module) => module.pptDeck?.id === deckId)?.getPptNotes?.(sceneId) ?? []}
  />;
}

export const appRoutes: AppRoute[] = [
  { path: '/', element: <HomePage /> },
  { path: '/shared/ui-kit', element: <UiKitPage /> },
  ...activeModules.flatMap((module) => [
    { path: module.path, element: module.element },
  ]),
  ...[
    { path: '/scenedeck/', element: <SceneDeckPage /> },
    { path: '/web_ppt/', element: <SceneDeckPage /> },
    { path: '/web_ppt/slide.html', element: <SceneDeckPage /> },
  ],
];

