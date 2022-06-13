$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

var notifications = true
var stations = []

function renderStations() {
  var html_string = ""
  stations.forEach((station) => {
    html_string += `
      <span onclick="removeStation('${station}')" class="badge badge-pill badge-light"><i class="material-icons mr-1" style="font-size:12px">close</i> ${station}</span>
    `
  })
  document.getElementById("stationBadges").innerHTML = html_string
}

function addStation() {
  stations.push(document.getElementById("newStationInput").value)
  renderStations()
  $('#newStationModal').modal('toggle')
  document.getElementById("newStationInput").value = ""

  fetchDisruptions()
}

function removeStation(station_to_remove) {
  stations = stations.filter(station => station !== station_to_remove)
  renderStations()

  fetchDisruptions()
}

function renderDisruptions(disruptions) {
  var html_string = ""
  disruptions.forEach((disruption) => {
    html_string += `
    <div class="card shadow-none border-bottom border-dark rounded-0">
      <div class="card-body">
        <h5 class="card-title">${disruption['title']}</h5>
        <p class="card-text">${disruption['situation']} ${disruption['expectedDuration']}</p>
        <a href="#" class="btn btn-danger">${disruption['additionalTravelTime']}</a>
      </div>
    </div>
    `
  })
  document.getElementById("disruptions").innerHTML = html_string + "<br><br><br><br>"
}

function fetchDisruptions() {
  if (stations.length>0) {
    showLoadingAnimation()
    pywebview.api.fetchDisruptions(stations).then((response) => {
      renderDisruptions(response)
    })
  } else {
    document.getElementById("disruptions").innerHTML = ""
  }
}

function showLoadingAnimation() {
  document.getElementById("disruptions").innerHTML = `
  <div class="w-100 d-flex justify-content-center align-items-center" style="min-height:calc(100% - 92px);max-height:calc(100% - 92px)">
    <div class="progress-circular progress-circular-warning" style="transform:scale(2)">
        <div class="progress-circular-wrapper">
            <div class="progress-circular-inner">
                <div class="progress-circular-left">
                    <div class="progress-circular-spinner"></div>
                </div>
                <div class="progress-circular-gap"></div>
                <div class="progress-circular-right">
                    <div class="progress-circular-spinner"></div>
                </div>
            </div>
        </div>
    </div>
  </div>
  `
}

function toggleNotifications() {
  pywebview.api.toggleNotifications()
  notifications = !notifications
  if (notifications) {
    document.getElementById("notificationIndicator").innerHTML = "notifications"
  } else {
    document.getElementById("notificationIndicator").innerHTML = "notifications_off"
  }
}

setInterval(() => {
  fetchDisruptions()
}, 1200000)