export type EmitSubmit = {
  (e: 'submit'): void
  (e: 'submit', id_project: number): void
}

export type EmitDelete = {
  (e: 'delete'): void
}

export type EmitItemSelected = {
  (e: 'itemSelected', selectedItem: any): void
}

export type EmitDialog = {
  (e: 'update:showDialog', showDialog: boolean): void
  (e: 'submit', data: any): void
  (e: 'delete'): void
}
