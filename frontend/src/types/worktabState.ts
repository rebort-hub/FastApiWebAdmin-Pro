import type { WorkTabItem } from './worktab'

export interface WorkTabState {
  opened: WorkTabItem[]
  activePath: string
}
