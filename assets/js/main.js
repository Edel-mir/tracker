tailwind.config = {
  darkMode: 'class',
}

const themeBtn = document.querySelector('#themeButton')

window.onload = function () {
  const theme = localStorage.getItem('theme')
  if (theme !== null) {
    setTheme(theme)
  } else {
    localStorage.setItem('theme', 'light')
  }
}

const setTheme = function (theme) {
  document.documentElement.classList = theme
}

themeBtn.addEventListener('click', function (e) {
  e.preventDefault()
  const theme = localStorage.getItem('theme')
  if (theme === 'dark') {
    localStorage.setItem('theme', 'light')
    setTheme('light')
  } else {
    localStorage.setItem('theme', 'dark')
    setTheme('dark')
  }
})
