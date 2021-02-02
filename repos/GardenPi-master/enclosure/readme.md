<h2 align="center">
  <a name="gardenpi_logo" href="https://github.com/rjsears/GardenPi"><img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_cover.jpg" alt="GardenPi" height="700" width="550"></a>
  <br>
  GardenPi (V1.0.0 - August 4th, 2020)
  </h2>
  <p align="center">
  Multizone Hydroponic / Aquaponic / Irrigation &amp; Fish Tank Water management and monitoring platform
  </p>
<h2 align="center">BOM For GardenPi</h2>

<div align="center"><a name="top_menu"></a>
  <h4>
    <a href="https://github.com/rjsears/GardenPi">
      Back to Main Read Me
    </a>
    </h4>
</div>

There are a <b><em>lot</em></b> of parts that went into building <b><em>our</em></b> version of GardenPi. GardenPi is designed to be scaled from a few zones to as many as 32 water zones or anywhere in between. Since you have to build your own enclosure, you can decide what parts of GardenPi meet your needs (such as the need for power control) and decide what you need from there. I love lots of data so I have sensors for AC and DC power, water utilization (albeit not from GardenPi), humidity, barometric pressure, etc. So when you view this parts list, keep in mind you may not need everything listed here and some are options (touchscreen, cover).
<hr>

### System Enclosure - Polycase YH-141206 NEMA Hinged Electrical Enclosure
The system enclosure that I chose was pretty large due to all of the parts that needed to fit inside. I chose not the cheapest enclosure, but one that would do the job for me.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_system_enclosure.jpg" alt="GardenPi System Enclosure" height="200" width="400"><br>
Purchase Location: <a href="https://www.polycase.com/yh-141206">Polycase.com</a><br>
Part Numbers Ordered:
<ul>
  <li>YH-141206-02 NEMA Hinged Electrical Enclosure - <b>$87.41</b></li>
  <li>SCREWS-011-100 PCB Screws for YH/YQ & ZH/ZQ Series Enclosures - <b>$3.82</b> </li>
  <li>YX-93 Panel Suspension Kit for YH/YQ Series Enclosures <b>$8.87</b></li>
  <li>2 x UA-023 80mm Large Fan Vents <b>$7.16/ea</b></li>
  <li>2 x YX-1412K Panel for YH/YQ Series Enclosures <b>$24.61/ea</b></li>
</ul>
<b>Total with Shipping/Tax: $181.62</b>
<br>
<hr>

### Canakit Raspberry Pi4 Model B - 4GB
You could get by with a lower powered version of the RaspberryPi, but I choose the Rpi4 with 4/GB RAM for this project.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/canakit_rpi_4.jpg" alt="GardenPi RPi4" height="200" width="250">
Purchase Location: <a href="https://www.amazon.com/gp/product/B07TC2BK1X/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$60.50</em></b>
<br><hr>

### Samsung Endurance Pro 128GB SD Card
I chose the Samsung Pro Endurance 128GB card for several reasons. First I have never had any issues with any Samsung SD card that I have purchased, next the Pro Endurance is designed to be a very long endurance card. The 128GB cards is rated to last up to 43,800 hours of continuous video recording, while the 64GB card was half that time. Since the 128GB card is good for a full 5 years of continuous video recording, I figured it would be good with the little bit GardenPi would be doing with it.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_samsung_pro.jpg" alt="GardenPi SD Card" height="100" width="150">
Purchase Location: <a href="https://www.amazon.com/Samsung-Endurance-128GB-Micro-Adapter/dp/B07B984HJ5">Amazon.com</a><br>
Purchase Price: <b><em>$28.99</em></b>
<br><hr>

### Geekworm Aluminum alloy Armor case with dual fans
I chose this case because I will need maximum cooling where I will be placing this system. My ambient temperature in the shed where my enclosure is installed can reach 135°F in the summer. I have had amazing luck running a Pi3B in 120-degree weather here in Phoenix for years with just a cooling fan in the overall enclosure for my pool control system. I will try this case out to see how well it works and how long the fans last. I track enclosure and Pi CPU temps every minute, I have not had an throttling issues as of yet, even on the hottest of days.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_geekwork_case.jpg" alt="GardenPi Case" height="175" width="250">
Purchase Location: <a href="https://smile.amazon.com/Geekworm-Raspberry-Computer-Aluminum-Compatible/dp/B07VD6LHS1/ref=sr_1_4?dchild=1&keywords=geekworm+case&qid=1596485916&s=electronics&sr=1-4">Amazon.com</a><br>
Purchase Price: <b><em>$17.89</em></b>
<br><hr>

### Sainsmart 5V 2A 8-Channel Solid State Relay Module (High Level Trigger) x 4
One thing I have learned in my past projects with a lot of electrical and sensors, mechanical relays can cause interference in various parts of the system. I chased a problem wit my pool control project where every time I triggered my mechanical relay, I would get weird reading and other glitches, even with optoisolated mechanical relays. I moved to solid-state relays and never looked back. These relays are 2A max which is more than enough to power a sprinkler valve.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_ss_relays_8.jpg" alt="GardenPi SS Relays" height="175" width="350">
Purchase Location: <a href="https://smile.amazon.com/gp/product/B00ZZW7MI6/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$17.89/each</em></b>
<br><hr>

### Sainsmart 5V 2A 2-Channel Solid State Relay Module
This relay drives my two AC fans in the enclosure.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_two_channel_relay.jpg" alt="GardenPi SS Relays" height="175" width="250">
Purchase Location: <a href="https://smile.amazon.com/SainSmart-2-Channel-Duemilanove-MEGA2560-MEGA1280/dp/B0079WI2ZC/ref=sr_1_25?crid=2XATJMBNW9EN0&dchild=1&keywords=sainsmart+relay+module&qid=1596487851&sprefix=sainsmart+relay%2Caps%2C205&sr=8-25">Amazon.com</a><br>
Purchase Price: <b><em>$13.99</em></b>
<br><hr>



### Emerson 90-T40F3 120V to 24V AC-to-AC transformer 
This transformer is used to power our sprinkler valves (27 of them). Most irrigation valves utilize AC due to the length of the wire runs, but there are some DC valves out there. If you are planning on using DC valves, the Sainsmart relays above <b>WILL NOT WORK</b> as these relays use <a href="https://www.electronics-notes.com/articles/electronic_components/scr/what-is-a-triac.php">Triacs</a>. They will only work for AC circuits. Read the notes <a href="https://www.sainsmart.com/products/8-channel-5v-2a-solid-state-relay-high-level-trigger">HERE</a> for more information!

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_transformer.jpg" alt="GardenPi Transformer" height="175" width="175">
Purchase Location: <a href="https://smile.amazon.com/dp/B00WGMX9TY?tag=amz-mkt-chr-us-20&ascsubtag=1ba00-01000-org00-mac00-other-smile-us000-pcomp-feature-scomp-wm-5&ref=aa_scomp_sosp1">Amazon.com</a><br>
Purchase Price: <b><em>$13.99</em></b>
<br><hr>

### Mean Well RS-25-5 AC-to-DC 5V, 5A Switching Power Supply
While the Canakit comes with a very nice 3A USB-C power supply, I will be running 27 relays and lot of other 3.3/5V boards and sensors, so I opted to get a 5A switched 5V power supply. I have had great luck with Mean Well over the years so that is why I chose this power supply.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_5V_power_supply.jpg" alt="GardenPi 5V Power Supply" height="175" width="250">
Purchase Location: <a href="https://www.digikey.com/product-detail/en/mean-well-usa-inc/RS-25-5/1866-4145-ND/7706180">DigiKey.com</a><br>
Purchase Price: <b><em>$11.54</em></b>
<br><hr>

### Potter Brumfield 15A, 120V push thru circuit breaker 
W28XQ1A-15. Used for AC circuit current protection.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_ac_circuit_brkr.jpg" alt="GardenPi AC Circuit Breaker" height="175" width="200">
Purchase Location: <a href="https://smile.amazon.com/Potter-Brumfield-Circuit-Breaker-W28XQ1A-15/dp/B002PXG1BC/ref=sr_1_1?dchild=1&keywords=W28XQ1A-15&qid=1596488260&sr=8-1">Amazon.com</a><br>
Purchase Price: <b><em>$7.25</em></b>
<br><hr>

### Black US 3-Pin Power Socket Plugs x 10
Thru panel mount standard 3-pole, 15A 120V plugs for plugging in equipment to be controlled by the GardenPi system. Bag of 10.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_110v_plugs.jpg" alt="GardenPi 120V Outlets" height="175" width="250">
Purchase Location: <a href="https://smile.amazon.com/gp/product/B01M3URWIT/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$8.99</em></b>
<br><hr>

### UBIDE IP67 Waterproof CAT5 RJ45 Feed-Thru Coupler
I will be utilizing a hard-wired ethernet connection and I want all connections into the enclosure to be thru-mount, waterproof and to look very nice.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_ethernet_jack.jpg" alt="GardenPi Ethernet Jack" height="175" width="250">
Purchase Location: <a href="https://smile.amazon.com/gp/product/B077C6W2MP/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$9.99</em></b>
<br><hr>

### Schurter 120V, 15A Power Entry connector
Provides a nice and clean way to connect a power cable to our enclosure. One of the very few 15A plug/switch combos that I was able to find.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_input_120v_outlet.jpg" alt="GardenPi AC Input Outlet" height="275" width="250">
Purchase Location: <a href="https://www.digikey.com/products/en?keywords=486-3013-ND">DigiKey.com</a><br>
Purchase Price: <b><em>$24.18</em></b>
<br><hr>

### SP21 Waterproof 9-Pin Thru-bulkhead heavy-duty connector x 8
These are used for all of sprinkler valve 24v AC wiring, non-contact liquid level sensors and ultrasonic liquid level sensors. For the latter two you can opt for the 8-Pin plugs but you need the 9-pin for the sprinkler valves. You need one connector for every 8 valves. <b><em>NOTE:</b> You will also need one additional for every plug (8 more) if you are running to zone/sensor extension boxes like I am doing. If you plan on wiring your zones/sensors directly to your enclosure, you will only need the 8.</em> 

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_9pin_plgs.jpg" alt="GardenPi 9-Pin Plug" height="250" width="350">
Purchase Location: <a href="https://www.amazon.com/gp/product/B07D8SJMG7/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1&pldnSite=1">Amazon.com</a><br>
Purchase Price: <b><em>$11.99/each</em></b>
<br><hr>

### SP21 Waterproof 3-Pin Thru-bulkhead heavy-duty connector x 2
This is used for our DS18B20 Onewire temperature probes. One set if for the enclosure and second set for the actual box that houses the temp probes. 

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_3pin_plug.jpg" alt="GardenPi 3-Pin Plug" height="250" width="350">
Purchase Location: <a href="https://smile.amazon.com/gp/product/B07D8XDYKY/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$11.99/each</em></b>
<br><hr>

### LowPowerLabs MightyHat
Very cool RaspberryPi power controller, UPS system and 433Mhz gateway. Provides full UPS and completely safe unattended shutdown of your Pi if you run out of battery power before power is restored. System displays messages on LCD screen as well.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_mightyhat.jpg" alt="GardenPi MightyHat" height="250" width="350">
Purchase Location: <a href="https://lowpowerlab.com/shop/mightyhat">LowPowerLabs.com</a><br>
Purchase Price: <b><em>$45.00</em></b>
<br><hr>

### Adafruit Industries 6.2AH 3.7V Lithium battery
Provides battery backup power to the MightyHat. Will run the Pi for several hours (if not more) in idle mode. 

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_backup_battery.jpg" alt="GardenPi Backup Battery" height="250" width="250">
Purchase Location: <a href="https://www.digikey.com/products/en?mpart=353&v=1528">DigiKey.com</a><br>
Purchase Price: <b><em>$29.50</em></b>
<br><hr>

### DFRobot Gravity: MCP23017 I2C 16 Digital IO Expansion Module x 4 
Adds 64 additional GPIO ports to the Raspberry Pi. Utilizes I2C in GardenPi. Everything that utilizes GPIOs in GardenPi are run from the MCP23017s.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_mcp23017.jpg" alt="GardenPi MCP23017" height="225" width="250">
Purchase Location: <a href="https://www.digikey.com/products/en?mpart=DFR0626&v=1738">DigiKey.com</a><br>
Purchase Price: <b><em>$4.55/each</em></b>
<br><hr>

### DFRobot Gravity: Non-contact Digital Water / Liquid Level Sensor For Arduino x 4
Utilized to monitor the water level in various tanks including fish water and hydroponic solutions. This sensor is what we use to make actual decisions.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_non-contact_sensor.jpg" alt="GardenPi NC Liquid Sensor" height="225" width="260">
Purchase Location: <a href="https://www.digikey.com/product-detail/en/dfrobot/SEN0204/SEN0204-ND/6579443">DigiKey.com</a><br>
Purchase Price: <b><em>$10.00/each</em></b>
<br><hr>

### DFRobot Gravity: I2C Bosch BME280 Environmental Sensor
Sensor to provide Temperature, humidity and barometric pressure inside our project enclosure. Used to determine when to run the onboard fans to cool the enclosure and provide enclosure environmental data for graphing.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_BME280.jpg" alt="GardenPi NC Liquid Sensor" height="225" width="260">
Purchase Location: <a href="https://www.digikey.com/products/en?keywords=SEN0236">DigiKey.com</a><br>
Purchase Price: <b><em>$15.78</em></b>
<br><hr>

### DFRobot Gravity: I2C Digital Wattmeter
High-resolution, high-precision measurement module to monitor the voltage and current usage of our 5V loads.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_DC_watt_meter.jpg" alt="GardenPi NC Liquid Sensor" height="200" width="220">
Purchase Location: <a href="https://www.amazon.com/Gravity-Wattmeter-Bi-Directional-Measurement-Breakout/dp/B07N3QQ2Q7">Amazon.com</a><br>
Purchase Price: <b><em>$11.90</em></b>
<br><hr>


### Adafruit 800x480 Touchscreen HDMI Display
System touchscreen interface display for GardenPi. Provided for local control.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_touchscreen.jpg" alt="GardenPi Touchscreen" height="200" width="220">
Purchase Location: <a href="https://www.adafruit.com/product/2407">Adafruit.com</a><br>
Purchase Price: <b><em>$89.95</em></b>
<br><hr>

### Front Panel Express Custom Panel Mount
I designed this panel in FrontDesign by Front Panel Express. This exactly fits the Adafruit 800x400 touchscreen display and provides a secure and nice way to mount the screen. It is painted aluminum and the wording is etched and painted.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_front_panel.jpg" alt="GardenPi Touchscreen Panel" height="400" width="420">
Purchase Location: <a href="frontpanelexpress.com">Frontpanelexpress.com</a><br>
Purchase Price: <b><em>$145.00</em></b>
<br><hr>

### Dallas DS18B20 Onewire Temperature Probes x 5
These are for monitoring temperatures in our worm farm along with water temps in our various tanks. I purchased these from DFRobot along with other things and they come with authentic Dallis chips.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_ds18b20.jpg" alt="GardenPi DS18B20" height="200" width="220">
Purchase Location: <a href="https://www.dfrobot.com/product-689.html">DFRobot.com</a><br>
Purchase Price: <b><em>$6.90/each</em></b>
<br><hr>

### Waveshare I2C Serial Expansion Module x 2
This module adds two additional serial ports to the Raspberry Pi. We need a total of four additional serial ports to talk to our Ultrasonic water level detectors. It also adds additional GPIOs, but I do not use them. Each module requires an inturrupt pin on the Pi.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_serial_expander.jpg" alt="GardenPi Serial Expander" height="200" width="250">
Purchase Location: <a href="https://www.amazon.com/gp/product/B07KCR3Y7W/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$18.99/each</em></b>
<br><hr>

### Inkbird 40A Solid State Relays x 8
These relays are used on the 120V side of GardenPi. One relay per outlet (7) and an additional relay to power our AC-to-AC transformer as opposed to having it powered on 24x7.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_40a_ss_relay.jpg" alt="GardenPi Serial Expander" height="200" width="175">
Purchase Location: <a href="https://www.amazon.com/gp/product/B07Y33RZ8F/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$11.50/each</em></b>
<br><hr>

### I2C Extender/Expander
This extender provides 8 x I2C ports for all of our IC2 connected components.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_i2c_expander.jpg" alt="GardenPi I2C Expander" height="100" width="175">
Purchase Location: <a href="https://www.ebay.com/itm/121200480686">EBay.com</a><br>
Purchase Price: <b><em>$15.95/each</em></b>
<br><hr>

### 120VAC Brushless Cooling Fan 80mm x 25mm x 2
These are AC powered 40CFM brushless cooling fans to help cool the system enclosure. These are connected to the two-port solid-state relay board and temperature controlled by GardenPi. 67,000 Hour lifespan.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_ac_fans.jpg" alt="GardenPi AC Fans" height="175" width="175">
Purchase Location: <a href="https://www.amazon.com/gp/product/B07SDDSCY1/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$18.99/each</em></b>
<br><hr>


### Power Distribution Screw Terminal Blocks x 10
These are very nice, small power distribution blocks. I use them for AC, DC and onewire connections.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_terminal_blocks.jpg" alt="GardenPi Terminal Blocks" height="175" width="300">
Purchase Location: <a href="https://www.ebay.com/vod/FetchOrderDetails?itemid=293062941310&transid=1804265334019&ul_noapp=true">EBay.com</a><br>
Purchase Price: <b><em>~$2.00/each</em></b>
<br><hr>

### 18/10 Black Solid UL Sprinkler System Wire
I run a cable from my enclosure to a "zone extension box" where I tie in all of my zones. This way I do not have to run every zone back to my enclosure. I also use this wire for all of my internal sprinkler-relay wiring in the enclosure. The total length you need will depend on how far your zones are and how far you extension boxes are located. 

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_1810.jpg" alt="GardenPi Sprinkler Wire" height="100" width="200">
Purchase Location: <a href="https://www.homedepot.com/p/Southwire-By-the-Foot-18-10-Black-Solid-UL-Sprinkler-System-Wire-49270299/204724972">HomeDepot.com</a><br>
Purchase Price: <b><em>$0.73/foot</em></b>
<br><hr>

### 18/4 Gray Stranded CU CL3R Shielded Security Cable
I use this wire to extend my onewire temperature probes as well as our ultrasonic sensors and non-contact liquid sensors.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_184.jpg" alt="GardenPi Security Wire" height="100" width="300">
Purchase Location: <a href="https://www.homedepot.com/p/Southwire-By-the-Foot-18-4-Gray-Stranded-CU-CL3R-Shielded-Security-Cable-57573099/204725141">HomeDepot.com</a><br>
Purchase Price: <b><em>$0.55/foot</em></b>
<br><hr>

### Carlon 4" x 4" x 2" Junction Box
I use these waterproof junction boxes as my "extenders". My zone and sensor cables leave my enclosure and run to these boxes. From there I extend to where I need the final runs.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_junction_extension_box.jpg" alt="GardenPi Junction Extension Box" height="170" width="200">
Purchase Location: <a href="https://www.homedepot.com/p/Carlon-4-in-x-4-in-x-2-in-PVC-Junction-Box-Gray-E989NNJ-CAR/100404097">HomeDepot.com</a><br>
Purchase Price: <b><em>$8.76/each</em></b>
<br><hr>

### Cable Glands - Various Sizes
If you are running your zone and sensor wiring to extension boxes like I am doing, then these cable glands are for your sensor/zone wiring to your extension boxes. Make sure you get the right sizes!

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_cable_glands.jpg" alt="GardenPi Cable Glands" height="170" width="200">
Purchase Location: <a href="https://www.adafruit.com/product/762">Adafruit.com</a><br>
Purchase Price: <b><em>$1.95/each</em></b>
<br><hr>


### Assorted heat shrink tubing
Used to protect solder joints.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_heat_shrink.jpg" alt="GardenPi Heat Shrink" height="275" width="175">
Purchase Location: <a href="https://www.homedepot.com/p/Gardner-Bender-3-in-Length-Assorted-Heat-Shrink-Black-Tubing-160-Kit-HST-ASTB/202797328">Home Depot.com</a><br>
Purchase Price: <b><em>$15.44/each</em></b>
<br><hr>

### 1/4 in. Fully Insulated Wire Disconnects in Blue (15-Pack) x 2
Used for AC power connection to internal enclosure 120V power outlets.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_wire_disconnects.jpg" alt="GardenPi Wie Disconnects" height="275" width="175">
Purchase Location: <a href="https://www.homedepot.com/p/Gardner-Bender-1-4-in-Fully-Insulated-Wire-Disconnects-in-Blue-15-Pack-15-153F/202521914">Home Depot.com</a><br>
Purchase Price: <b><em>$3.23/box</em></b>
<br><hr>

### 32 Red In-Sure 2-Port Connectors (100-Pack)
I use this type of wire connectors in my external zone/sensor extension boxes to connect the internal wiring. I prefer these to wire nuts. 

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_wire_connectors.jpg" alt="GardenPi Wire Connectors" height="125" width="175">
Purchase Location: <a href="https://www.homedepot.com/p/Ideal-32-Red-In-Sure-2-Port-Connectors-100-Pack-30-1032P/202894308">Home Depot.com</a><br>
Purchase Price: <b><em>$7.32/package</em></b>
<br><hr>

### 260 Pcs M3 Hex Socket Flat Head Countersunk Bolts Screw Nut Assortment Kit-304 Stainless Steel
For anything that has to be screwed from the outside or bottom, I use these countersunk stainless steel screws.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_countersunk_screws.jpg" alt="GardenPi Countersunk Screws" height="300" width="300">
Purchase Location: <a href="https://www.amazon.com/gp/product/B076J3W7R4/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$12.99</em></b>
<br><hr>

### 240 Pieces M3 Male Female Hex Brass Spacer Standoff Screw Nut Threaded Pillar PCB Motherboard Assortment Kit x 2
Used to mount all sensors, relays, terminal blocks, etc to the inside of the enclosure plates.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_standoff_kit.jpg" alt="GardenPi Countersunk Screws" height="150" width="300">
Purchase Location: <a href="https://www.amazon.com/gp/product/B07PK23VC4/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1">Amazon.com</a><br>
Purchase Price: <b><em>$13.99/each</em></b>
<br><hr>

### Orbit 3/4 in. Plastic FPT Automatic Anti-Siphon Zone Valve (24VAC)
These are the sprinkler/anti-siphon valves I use for the entire project.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gradenpi_sprinkler_valves.jpg" alt="GardenPi Sprinkler Valves" height="275" width="300">
Purchase Location: <a href="https://www.homedepot.com/p/Orbit-3-4-in-Plastic-FPT-Automatic-Anti-Siphon-Zone-Valve-57623/203020016">HomeDepot.com</a><br>
Purchase Price: <b><em>$15.44/each</em></b>
<br><hr>

### IWAKI MD-70RLT - 1536 GPH Water Pump (Japanese Motor)
These pumps are used for water pumping and circulation.

<img src="https://github.com/rjsears/GardenPi/blob/master/images/gardenpi_circulation_pumps.jpg" alt="GardenPi Water Pump" height="200" width="300">
Purchase Location: <a href="https://www.fishtanksdirect.com/iwaki-pumps-md-70rlt-aquarium-pump-iw00700.aspx">FishTanksDirect.com</a><br>
Purchase Price: <b><em>$367.19/each</em></b>
<br><hr>


