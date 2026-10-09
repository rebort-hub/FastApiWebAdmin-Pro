
export interface TreeNodeLike {
  id?: number
  parent_id?: number | null
  children?: this[]
}
