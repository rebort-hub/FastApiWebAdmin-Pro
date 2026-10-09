export interface loginFormType {
  username: string
  password: string
  captcha: string
  captcha_key: string
  remember: boolean
  [key: string]: string | boolean
}

export interface captchaStateType {
  enable: boolean;
  key: string;
  img_base: string;
}