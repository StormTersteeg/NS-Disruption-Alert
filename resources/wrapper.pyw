import webview, os, sys, requests, uuid
from win10toast import ToastNotifier

# define event handlers
def on_closed():
  pass

def on_closing():
  pass

def on_shown():
  pass

def on_loaded():
  pass

class Api:
  def __init__(self):
    self.notify = True
    self.ocp_apim_subscription_key = "{settings.ocp_apim_subscription_key}"

  def openChild(self, url):
    window.hide()
    child = webview.create_window(url, url)

  def minimize(self):
    window.minimize()

  def fullscreen(self):
    window.toggle_fullscreen()

  def close(self):
    window.destroy()

  def reload(self):
    os.startfile(sys.argv[0])
    self.close()

  def toggleNotifications(self):
    self.notify = not self.notify
    if self.notify:
      toaster.show_toast("NS Disruption Alert", f"Notificaties Aan", icon_path='', threaded=True)
    else:
      toaster.show_toast("NS Disruption Alert", f"Notificaties Uit", icon_path='', threaded=True)

  def fetchDisruptions(self, stations):
    disruption_data = []

    # request used to fetch disruption data
    url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/disruptions"
    headers = {
      "Ocp-Apim-Subscription-Key": self.ocp_apim_subscription_key,
      "X-Request-Id": str(uuid.uuid4()),
    }
    response = requests.get(url, headers=headers)

    # scan all the disruption data for our selected stations, add them to the disruption_data if present
    for storing in response.json():
      try:
        if any(station in storing['title'] for station in stations):
          disruption = {
            "title": storing['title'],
            "situation": storing['timespans'][0]['situation']['label'],
            "additionalTravelTime": storing['summaryAdditionalTravelTime']['shortLabel'],
            "expectedDuration": storing['expectedDuration']['description'] if "expectedDuration" in storing else ""
          }
          disruption_data.append(disruption)
      except: pass
    
    if self.notify and len(disruption_data)>0:
      toaster.show_toast("NS Disruption Alert", f"Vertraging gevonden op 1 van jouw stations", icon_path='', threaded=True)
    return disruption_data

#!FLAG-HTML

if __name__ == '__main__':
  api = Api()
  toaster = ToastNotifier()
  window = webview.create_window("{settings.app_name}", html=html, js_api=api, width={settings.app_proportions[0]}, height={settings.app_proportions[1]}, confirm_close={settings.app_confirm_close}, frameless={settings.app_frameless}, fullscreen={settings.app_fullscreen}, resizable={settings.app_resizable})
  window.events.closed += on_closed
  window.events.closing += on_closing
  window.events.shown += on_shown
  window.events.loaded += on_loaded
  webview.start(gui="{settings.app_web_engine}", debug={settings.app_allow_inspect})