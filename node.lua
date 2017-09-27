gl.setup(NATIVE_WIDTH, NATIVE_HEIGHT)

local json = require "json"
local font = resource.load_font "font.ttf"
local fontbold = resource.load_font "fontbold.ttf"

node.alias "KenticoCloud"
local current_image = resource.load_image("image.jpg")
local red = resource.load_image("red.png")
local wifierror = resource.load_image("nowifi.png")
local cloud_img_name = ""
local elements = {}
local counter = 0
local cache = false
local coffeeElements = {}
local lines = {}
local image_height = HEIGHT
local image_width = WIDTH
local image_align = 0 
local text_align = WIDTH / 2
util.data_mapper{
	
	update = function(elements)
		coffeeElements = json.decode(elements)
		for idx, element in ipairs(coffeeElements) do
			print("element.photo coming up")
			print(element.photo)
			local image = string.format("%s", element.photo)
			cloud_img_name = image
			current_image = resource.load_image(cloud_img_name)
		end
		
		if image_align == 0 then
			image_align = WIDTH / 2
			text_align = 100
		else
			image_align = 0
			text_align = WIDTH / 2 + 20
		end
		image_width = WIDTH / 2 + image_align
		--print(image_align)
	end
}

function node.render()
	gl.clear(1,1,1,1)
	current_image:draw(image_align,0,image_width,HEIGHT)

	for idx, element in ipairs(coffeeElements) do
		WriteSlide(element)
	end


end

function WriteSlide(element)
        local y = 200

 	--font:write(text_align, 10, "New Brews", 100, .1,.1,.1,1)
	--font:write(30, 110, "Demo Time", 100, .5,.5,.5,1)
        local productName = string.format("%s", element.coffee_name)
        fontbold:write(text_align, y, productName, 75, .1,.1,.1,1)
    	y = y + 150

	

        local shortDescription = string.format("%s", element.short_description)
	shortDescription = shortDescription:gsub("%b<>","")
	lines = wrap(shortDescription, 35)
	
	local size = 50	
    	for i, line in ipairs(lines) do
        	font:write(text_align, y, line, size, .1, .1, .1, 1)
        	y = y + size
    	end	
	y = y + size
	
	--local farm = string.format("%s",element.farm)
	--farm = farm:gsub("%b<>","")
	--font:write(text_align, y, "Farm:", size, .1,.1,.1,1)
	--y = y + size

	--font:write(text_align, y, farm, size, .1,.1,.1,1)
	--y = y + size + size
        
	--local country = string.format("%s",element.country)
	--font:write(text_align,y, "Country: " .. country, size,.1,.1,.1,1)
	--y = y + size 	

	local variety = string.format("%s", element.variety)
	font:write(text_align,y, "Variety: " .. variety, size,.1,.1,.1,1)
	y = y + size + size
	local price = string.format("%s" ,element.price) .. " / 1lb"
	fontbold:write(text_align ,y, price, 50,.1,.1,.1,1)
	y = y +100
	local processing = string.format("%s", element.processing)
	fontbold:write(text_align,y, processing, size,.6,.6,.6,1)
	local promotion = string.format("%s", element.promotion)
	if promotion == "Featured" then
		red:draw(20,20,800,100)
		font:write(130,35,"This Week's Featured Blend",50,1,1,1,1)
	end
	if element.wifiError == true then
		wifierror:draw(0,0,50,50)
	end
end


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
