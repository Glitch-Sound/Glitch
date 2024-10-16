export type EmitType<T = any> = {
  (event: string, payload?: T): void
}
