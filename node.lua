gl.setup(NATIVE_WIDTH, NATIVE_HEIGHT)

local json = require "json"
local font = resource.load_font "font.ttf"
local current_image = resource.load_image("image.jpg")
local cloud_img_name = ""
local elements = {}
local counter = 0
local cache = false

node.alias "KenticoCloud"

local lines = {}

function wrap(str, limit, indent, indent1)
    indent = indent or ""
    indent1 = indent1 or indent
    limit = limit or 72
    function wrap_parargraph(str)
        local here = 1-#indent1
        return indent1..str:gsub("(%s+)()(%S+)()", function(sp, st, word, fi)
            if fi-here > limit then
                here = st - #indent
                return "\n"..indent..word
            end
        end)
    end
    local splitted = {}
    for par in string.gmatch(str, "[^\n]+") do
        local wrapped = wrap_parargraph(par)
        for line in string.gmatch(wrapped, "[^\n]+") do
            splitted[#splitted + 1] = line
        end
    end
    return splitted
end

local CloudData
util.file_watch("CloudData.json", function(content)
	elements = json.decode(content)
	
	for idx, element in ipairs(elements) do
		local line4 = string.format("%s", element.background)
		cloud_img_name = line4
	end
	current_image = resource.load_image(cloud_img_name)
	
end)
pp(CloudData)

function node.render()
    local y = 300
    for idx, element in ipairs(elements) do

	cloud_img_name = line4

  	current_image:draw(0,0,WIDTH,HEIGHT)
 	font:write(500, 10, "Dancing Goat Events", 100, 1,1,1,1)
	--font:write(30, 110, "Demo Time", 100, .5,.5,.5,1)
        local line = string.format("%s", element.title)
        font:write(WIDTH / 2, y, line, 50, 1,1,.3,1)
    	y = y + 50
	local eventDate = string.format("%s" ,element.eventDate) 
	--eventDate = os.date("%c", eventDate)
	font:write(WIDTH / 2 ,y, eventDate, 50,1,1,1,1)
	y = y +100
        local line2 = string.format("%s", element.overlay)
	line2 = line2:gsub("%b<>","")
	lines = wrap(line2, 35)
	
	local size = 50	
    	for i, line in ipairs(lines) do
        	font:write(WIDTH / 2, y, line, size, 1, 1, 1, 1)
        	y = y + size
    	end	
	y = y + size
	
	local phoneNumber = "Phone Number: " .. string.format("%s",element.contactPhone)
	phoneNumber = phoneNumber:gsub("%b<>","")
	font:write(WIDTH /2, y, phoneNumber, size, 1,1,1,1)
	y = y + size + size
	local contactEmail = string.format("%s",element.contactEmail)
	font:write(WIDTH / 2,y, "Email: " .. contactEmail, size,1,1,1,1)	
   end
	counter = counter + 1

    
end


