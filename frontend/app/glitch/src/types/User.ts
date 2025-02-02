export interface User {
  rid: number
  user: string
  name: string
  is_admin: number
}

export interface UserCreate {
  user: string
  password: string
  name: string
  is_admin: number
}

export interface UserUpdate {
  rid: number
  user: string
  password: string
  name: string
  is_admin: number
}

export interface Login {
  user: string
  password: string
}

export interface MemberCreate {
  rid: number
}
