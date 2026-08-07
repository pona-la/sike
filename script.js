document.addEventListener('DOMContentLoaded', function () {
  const nasaLink = document.getElementById('nasa')
  const links = document.querySelectorAll('#peoplelist a')
  if (!nasaLink || !links.length)
    return
  const randomUrl = function () { return links[Math.floor(Math.random() * links.length)].href }
  const redirectIfHash = function () { if (location.hash == '#nasa') { location.hash = '', location.href = randomUrl() }}

  redirectIfHash()
  if (navigation) {
    navigation.addEventListener('navigatesuccess', redirectIfHash)
  } else {
    nasaLink.addEventListener('click', function () { location.href = randomUrl() })
  }
})