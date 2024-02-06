# SPDX-License-Identifier: CC0-1.0

:local domains [:toarray "home.arpa,johntron.com"]
:local dnsttl "15m"

:local magiccomment "automatic-from-dhcp (magic comment)"
:local activehosts [:toarray ""]

:foreach lease in [/ip dhcp-server lease find] do={
  :local hostname [/ip dhcp-server lease get value-name=host-name $lease]
  :local hostaddr [/ip dhcp-server lease get value-name=address $lease]

  :if ([:len $hostname] > 0) do={
    :foreach domain in $domains do={
      :local regdomain "$hostname.$domain"
      :set activehosts ($activehosts, $regdomain)

      :if ([:len [/ip dns static find where name=$regdomain]] = 0) do={
        :log info "Creating $regdomain $hostaddr"
        /ip dns static add name=$regdomain address=$hostaddr comment=$magiccomment ttl=$dnsttl
      } else={
        :if ([:len [/ip dns static find where name=$regdomain comment=$magiccomment]] = 1) do={
          :log info "Updating $regdomain $hostaddr"
          /ip dns static set address=$hostaddr [/ip dns static find name=$regdomain comment=$magiccomment]
        }
      }
    }
  }
}

:foreach dnsentry in [/ip dns static find where comment=$magiccomment] do={
  :local hostname [/ip dns static get value-name=name $dnsentry]
  :if ([:type [:find $activehosts $hostname]] = "nil") do={
    /ip dns static remove $dnsentry
  }
}