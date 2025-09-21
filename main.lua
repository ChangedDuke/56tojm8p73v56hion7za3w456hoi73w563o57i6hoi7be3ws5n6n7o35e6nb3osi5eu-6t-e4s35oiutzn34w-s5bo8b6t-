-- Coño Modz - Murder Mystery 2 Script
-- guns.lol/xup

-- Game Check System
local MM2_PLACE_ID = 142823291

if game.PlaceId ~= MM2_PLACE_ID then
    game.Players.LocalPlayer:Kick("Wrong Game. Go in Murder Mystery 2!")
    return
end

-- Services
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local TweenService = game:GetService("TweenService")
local VoiceChatService = game:GetService("VoiceChatService")
local TeleportService = game:GetService("TeleportService")
local VirtualUser = game:GetService("VirtualUser")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local StarterGui = game:GetService("StarterGui")
local Workspace = game:GetService("Workspace")

-- Local Player
local LocalPlayer = Players.LocalPlayer
local Camera = workspace.CurrentCamera

-- Script Settings
local settings = {
    espEnabled = false,
    noClipEnabled = false,
    rainbowTextEnabled = true,
    antiAFKEnabled = false,
    menuVisible = false
}

-- UI Elements
local keybindsGui = nil
local mainMenu = nil
local menuFrame = nil

-- Notification Function
local function notify(title, text, buttonText)
    StarterGui:SetCore("SendNotification", {
        Title = title,
        Text = text,
        Duration = 3,
        Button1 = buttonText or "Okay"
    })
end

-- ESP Functions
local function getPlayerColor(player)
    local character = player.Character or player.CharacterAdded:Wait()
    if not character then return Color3.fromRGB(0, 255, 0) end
    
    local backpack = player:FindFirstChild("Backpack")
    if not backpack then return Color3.fromRGB(0, 255, 0) end
    
    -- Check for weapons
    for _, tool in pairs(backpack:GetChildren()) do
        if tool:IsA("Tool") then
            local toolName = tool.Name:lower()
            if toolName:find("knife") then
                return Color3.fromRGB(255, 0, 0) -- Red for murderer
            elseif toolName:find("revolver") or toolName:find("pistol") or toolName:find("gun") or toolName:find("Gun") then
                return Color3.fromRGB(0, 0, 255) -- Blue for sheriff
            end
        end
    end
    
    -- Check character tools
    if character:FindFirstChildOfClass("Tool") then
        local tool = character:FindFirstChildOfClass("Tool")
        local toolName = tool.Name:lower()
        if toolName:find("knife") then
            return Color3.fromRGB(255, 0, 0) -- Red for murderer
        elseif toolName:find("revolver") or toolName:find("pistol") or toolName:find("gun") then
            return Color3.fromRGB(0, 0, 255) -- Blue for sheriff
        end
    end
    
    return Color3.fromRGB(0, 255, 0) -- Green for innocents
end

local function createESP(player)
    local billboard = Instance.new("BillboardGui")
    billboard.Name = "ESP_" .. player.Name
    billboard.Adornee = player.Character and player.Character:FindFirstChild("Head")
    billboard.Size = UDim2.new(0, 120, 0, 25)
    billboard.StudsOffset = Vector3.new(0, 2.5, 0)
    billboard.AlwaysOnTop = true
    billboard.MaxDistance = 1000
    
    local textLabel = Instance.new("TextLabel")
    textLabel.Size = UDim2.new(1, 0, 1, 0)
    textLabel.BackgroundTransparency = 1
    textLabel.Text = player.Name
    textLabel.TextColor3 = getPlayerColor(player)
    textLabel.TextScaled = true
    textLabel.Font = Enum.Font.SourceSansBold
    textLabel.Parent = billboard
    
    billboard.Parent = player.Character and player.Character:FindFirstChild("Head") or nil
    
    -- Update color when character changes
    player.CharacterAdded:Connect(function(character)
        wait(0.5)
        billboard.Adornee = character:FindFirstChild("Head")
        billboard.Parent = character:FindFirstChild("Head")
        textLabel.TextColor3 = getPlayerColor(player)
    end)
    
    return billboard
end

local function updateESPColors()
    for _, player in pairs(Players:GetPlayers()) do
        if player ~= LocalPlayer then
            local esp = player.Character and player.Character:FindFirstChild("ESP_" .. player.Name)
            if esp and esp:FindFirstChild("TextLabel") then
                esp.TextLabel.TextColor3 = getPlayerColor(player)
            end
        end
    end
end

local function removeESP()
    for _, player in pairs(Players:GetPlayers()) do
        if player ~= LocalPlayer then
            -- Suche im Character
            if player.Character then
                local esp = player.Character:FindFirstChild("ESP_" .. player.Name)
                if esp then esp:Destroy() end
                
                -- Suche auch im Kopf spezifisch
                local head = player.Character:FindFirstChild("Head")
                if head then
                    local headESP = head:FindFirstChild("ESP_" .. player.Name)
                    if headESP then headESP:Destroy() end
                end
            end
            
            -- Suche im gesamten Spieler-Objekt
            local playerESP = player:FindFirstChild("ESP_" .. player.Name)
            if playerESP then playerESP:Destroy() end
        end
    end
end

local function toggleESP()
    settings.espEnabled = not settings.espEnabled
    
    if settings.espEnabled then
        notify("Coño Mod Menu", "ESP: ON", "Okay")
        -- Deaktiviere alle vorhandenen ESP
        removeESP()
        
        -- Erstelle ESP für alle Spieler
        for _, player in pairs(Players:GetPlayers()) do
            if player ~= LocalPlayer then
                createESP(player)
            end
        end
        
        -- Update colors periodically
        spawn(function()
            while settings.espEnabled do
                updateESPColors()
                wait(1)
            end
        end)
    else
        notify("Coño Mod Menu", "ESP: OFF", "Okay")
        removeESP()
    end
end

-- NoClip Functions
local function toggleNoClip()
    settings.noClipEnabled = not settings.noClipEnabled
    
    if settings.noClipEnabled then
        notify("Coño Mod Menu", "NoClip enabled", "Okay")
        local character = LocalPlayer.Character or LocalPlayer.CharacterAdded:Wait()
        if character then
            for _, part in pairs(character:GetDescendants()) do
                if part:IsA("BasePart") then
                    part.CanCollide = false
                end
            end
        end
        
        -- Keep NoClip active
        spawn(function()
            while settings.noClipEnabled do
                local character = LocalPlayer.Character
                if character then
                    for _, part in pairs(character:GetDescendants()) do
                        if part:IsA("BasePart") then
                            part.CanCollide = false
                        end
                    end
                end
                wait()
            end
        end)
    else
        notify("Coño Mod Menu", "NoClip disabled", "Okay")
        -- Restore collision
        local character = LocalPlayer.Character
        if character then
            for _, part in pairs(character:GetDescendants()) do
                if part:IsA("BasePart") then
                    part.CanCollide = true
                end
            end
        end
    end
end

-- Kill Sheriff Functions
local function killSheriff()
    for _, player in pairs(Players:GetPlayers()) do
        if player ~= LocalPlayer then
            local character = player.Character
            if character then
                local backpack = player:FindFirstChild("Backpack")
                if backpack then
                    for _, tool in pairs(backpack:GetChildren()) do
                        if tool:IsA("Tool") then
                            local toolName = tool.Name:lower()
                            if toolName:find("revolver") or toolName:find("pistol") or toolName:find("gun") then
                                -- Found sheriff, kill them
                                local humanoid = character:FindFirstChild("Humanoid")
                                if humanoid then
                                    humanoid.Health = 0
                                    notify("Coño Mod Menu", "Sheriff killed!", "Nice")
                                    return true
                                end
                            end
                        end
                    end
                end
                
                -- Check if holding weapon
                if character:FindFirstChildOfClass("Tool") then
                    local tool = character:FindFirstChildOfClass("Tool")
                    local toolName = tool.Name:lower()
                    if toolName:find("revolver") or toolName:find("pistol") or toolName:find("gun") then
                        local humanoid = character:FindFirstChild("Humanoid")
                        if humanoid then
                            humanoid.Health = 0
                            notify("Coño Mod Menu", "Sheriff killed!", "Nice")
                            return true
                        end
                    end
                end
            end
        end
    end
    notify("Coño Mod Menu", "No sheriff found!", "Okay")
    return false
end

-- Attach to Sheriff Functions (Verbessert mit Teleport)
local function attachToSheriff()
    for _, player in pairs(Players:GetPlayers()) do
        if player ~= LocalPlayer then
            local character = player.Character
            local localCharacter = LocalPlayer.Character
            
            if character and character:FindFirstChild("HumanoidRootPart") and localCharacter and localCharacter:FindFirstChild("HumanoidRootPart") then
                local backpack = player:FindFirstChild("Backpack")
                if backpack then
                    for _, tool in pairs(backpack:GetChildren()) do
                        if tool:IsA("Tool") then
                            local toolName = tool.Name:lower()
                            if toolName:find("revolver") or toolName:find("pistol") or toolName:find("gun") then
                                -- Found sheriff, teleport to them first
                                local sheriffRoot = character.HumanoidRootPart
                                local localRoot = localCharacter.HumanoidRootPart
                                
                                -- Teleport to sheriff
                                localRoot.CFrame = sheriffRoot.CFrame * CFrame.new(0, 0, 3)
                                notify("Coño Mod Menu", "Teleported to sheriff!", "Nice")
                                    
                                    wait(0.2) -- Kurze Pause vor dem Anhaften
                                    
                                    -- Dann anhaften
                                    local humanoid = localCharacter:FindFirstChild("Humanoid")
                                    if humanoid then
                                        humanoid.Sit = true
                                        
                                        local localAttachment = Instance.new("Attachment")
                                        localAttachment.Parent = localRoot
                                        
                                        local sheriffAttachment = Instance.new("Attachment")
                                        sheriffAttachment.Parent = sheriffRoot
                                        
                                        local alignPosition = Instance.new("AlignPosition")
                                        alignPosition.Attachment0 = localAttachment
                                        alignPosition.Attachment1 = sheriffAttachment
                                        alignPosition.MaxForce = 10000
                                        alignPosition.Parent = localRoot
                                        
                                        local alignOrientation = Instance.new("AlignOrientation")
                                        alignOrientation.Attachment0 = localAttachment
                                        alignOrientation.Attachment1 = sheriffAttachment
                                        alignOrientation.MaxTorque = 5000
                                        alignOrientation.Parent = localRoot
                                        
                                        notify("Coño Mod Menu", "Attached to sheriff!", "Nice")
                                    
                                    wait(5)
                                    
                                    -- Clean up
                                    alignPosition:Destroy()
                                    alignOrientation:Destroy()
                                    localAttachment:Destroy()
                                    sheriffAttachment:Destroy()
                                    humanoid.Sit = false
                                    
                                    return true
                                end
                            end
                        end
                    end
                end
                
                -- Check if holding weapon
                if character:FindFirstChildOfClass("Tool") then
                    local tool = character:FindFirstChildOfClass("Tool")
                    local toolName = tool.Name:lower()
                    if toolName:find("revolver") or toolName:find("pistol") or toolName:find("gun") then
                        -- Found sheriff, teleport to them first
                        local sheriffRoot = character.HumanoidRootPart
                        local localRoot = localCharacter.HumanoidRootPart
                        
                        -- Teleport to sheriff
                        localRoot.CFrame = sheriffRoot.CFrame * CFrame.new(0, 0, 3)
                        notify("Coño Mod Menu", "Teleported to sheriff!", "Nice")
                            
                            wait(0.2) -- Kurze Pause vor dem Anhaften
                            
                            -- Dann anhaften
                            local humanoid = localCharacter:FindFirstChild("Humanoid")
                            if humanoid then
                                humanoid.Sit = true
                                
                                local localAttachment = Instance.new("Attachment")
                                localAttachment.Parent = localRoot
                                
                                local sheriffAttachment = Instance.new("Attachment")
                                sheriffAttachment.Parent = sheriffRoot
                                
                                local alignPosition = Instance.new("AlignPosition")
                                alignPosition.Attachment0 = localAttachment
                                alignPosition.Attachment1 = sheriffAttachment
                                alignPosition.MaxForce = 10000
                                alignPosition.Parent = localRoot
                                
                                local alignOrientation = Instance.new("AlignOrientation")
                                alignOrientation.Attachment0 = localAttachment
                                alignOrientation.Attachment1 = sheriffAttachment
                                alignOrientation.MaxTorque = 5000
                                alignOrientation.Parent = localRoot
                                
                                notify("Coño Mod Menu", "Attached to sheriff!", "Nice")
                            
                            wait(5)
                            
                            -- Clean up
                            alignPosition:Destroy()
                            alignOrientation:Destroy()
                            localAttachment:Destroy()
                            sheriffAttachment:Destroy()
                            humanoid.Sit = false
                            
                            return true
                        end
                    end
                end
            end
        end
    end
    notify("Coño Mod Menu", "No sheriff found!", "Okay")
    return false
end

-- Voice Chat Functions
local function spoofVoiceChat()
    -- Real Voice Chat spoof using actual VoiceChatService
    local success, error = pcall(function()
        -- Try to join voice chat properly
        if VoiceChatService then
            -- Method 1: Direct join
            VoiceChatService:joinVoice()
            
            -- Method 2: Alternative approach
            game:GetService("VoiceChatService"):joinVoice()
            
            notify("Voice Chat", "Voice Chat Spoof successful!", "Nice")
            return true
        end
    end)
    
    if not success then
        notify("Coño Mod Menu", "Voice Chat Spoof failed", "Okay")
    end
end

-- Server Switch Functions
local function serverSwitch()
    local currentPlaceId = game.PlaceId
    TeleportService:Teleport(currentPlaceId, LocalPlayer)
    notify("Coño Mod Menu", "Switching server...", "Okay")
end

-- Anti AFK Functions
local function toggleAntiAFK()
    settings.antiAFKEnabled = not settings.antiAFKEnabled
    
    if settings.antiAFKEnabled then
        notify("Coño Mod Menu", "Anti AFK enabled", "Okay")
        spawn(function()
            while settings.antiAFKEnabled do
                local success, error = pcall(function()
                    VirtualUser:CaptureController()
                    VirtualUser:ClickButton1(Vector2.new(0, 0))
                end)
                wait(30) -- Every 30 seconds
            end
        end)
    else
        notify("Coño Mod Menu", "Anti AFK disabled", "Okay")
    end
end

-- Spawn Knife Functions
local function spawnKnife()
    local character = LocalPlayer.Character
    if not character then 
        notify("Coño Mod Menu", "Character not found!", "Okay")
        return false 
    end
    
    local backpack = LocalPlayer:FindFirstChild("Backpack")
    if not backpack then 
        notify("Coño Mod Menu", "Backpack not found!", "Okay")
        return false 
    end
    
    -- Try to spawn a real knife
    local success, error = pcall(function()
        -- Look for existing knife in workspace or replicated storage
        local knifeTemplate = nil
        
        -- Check ReplicatedStorage for knife models (prioritize real game knives)
        for _, item in pairs(ReplicatedStorage:GetDescendants()) do
            if item:IsA("Tool") then
                local toolName = item.Name:lower()
                if toolName:find("knife") or toolName:find("blade") or toolName:find("dagger") then
                    knifeTemplate = item
                    break
                end
            end
        end
        
        -- If not found in ReplicatedStorage, check workspace
        if not knifeTemplate then
            for _, item in pairs(workspace:GetDescendants()) do
                if item:IsA("Tool") then
                    local toolName = item.Name:lower()
                    if toolName:find("knife") or toolName:find("blade") or toolName:find("dagger") then
                        knifeTemplate = item
                        break
                    end
                end
            end
        end
        
        -- If we found a knife template, clone it
        if knifeTemplate then
            local newKnife = knifeTemplate:Clone()
            
            -- Ensure the knife has proper properties
            if not newKnife:FindFirstChild("Handle") then
                local handle = Instance.new("Part")
                handle.Name = "Handle"
                handle.Size = Vector3.new(0.2, 1, 0.2)
                handle.Parent = newKnife
            end
            
            newKnife.Parent = backpack
            notify("Coño Mod Menu", "Knife spawned successfully!", "Nice")
            return true
        else
            -- Try to find any tool and modify it to be a knife
            for _, item in pairs(ReplicatedStorage:GetDescendants()) do
                if item:IsA("Tool") and item:FindFirstChild("Handle") then
                    local newKnife = item:Clone()
                    newKnife.Name = "Knife"
                    newKnife.Parent = backpack
                    notify("Coño Mod Menu", "Knife spawned from existing tool!", "Nice")
                    return true
                end
            end
            
            notify("Coño Mod Menu", "No knife template found!", "Okay")
            return false
        end
    end)
    
    if not success then
        notify("Coño Mod Menu", "Knife spawn failed: " .. tostring(error), "Okay")
        return false
    end
end

-- Spawn Gun Functions (Neu - für Murder Gun)
local function spawnGun()
    local character = LocalPlayer.Character
    if not character then 
        notify("Coño Mod Menu", "Character not found!", "Okay")
        return false 
    end
    
    local backpack = LocalPlayer:FindFirstChild("Backpack")
    if not backpack then 
        notify("Coño Mod Menu", "Backpack not found!", "Okay")
        return false 
    end
    
    -- Try to spawn a real gun (Murder Gun)
    local success, error = pcall(function()
        -- Look for existing gun in workspace or replicated storage
        local gunTemplate = nil
        
        -- Check ReplicatedStorage for gun models (prioritize real game guns)
        for _, item in pairs(ReplicatedStorage:GetDescendants()) do
            if item:IsA("Tool") then
                local toolName = item.Name:lower()
                if toolName:find("gun") or toolName:find("revolver") or toolName:find("pistol") or toolName:find("weapon") then
                    gunTemplate = item
                    break
                end
            end
        end
        
        -- If not found in ReplicatedStorage, check workspace
        if not gunTemplate then
            for _, item in pairs(workspace:GetDescendants()) do
                if item:IsA("Tool") then
                    local toolName = item.Name:lower()
                    if toolName:find("gun") or toolName:find("revolver") or toolName:find("pistol") or toolName:find("weapon") then
                        gunTemplate = item
                        break
                    end
                end
            end
        end
        
        -- If we found a gun template, clone it
        if gunTemplate then
            local newGun = gunTemplate:Clone()
            
            -- Ensure the gun has proper properties
            if not newGun:FindFirstChild("Handle") then
                local handle = Instance.new("Part")
                handle.Name = "Handle"
                handle.Size = Vector3.new(0.3, 0.8, 1.2)
                handle.Parent = newGun
            end
            
            newGun.Parent = backpack
            notify("Coño Mod Menu", "Real gun spawned successfully!", "Nice")
            return true
        else
            -- Try to find any tool and modify it to be a gun
            for _, item in pairs(ReplicatedStorage:GetDescendants()) do
                if item:IsA("Tool") and item:FindFirstChild("Handle") then
                    local newGun = item:Clone()
                    newGun.Name = "Gun"
                    newGun.Parent = backpack
                    notify("Coño Mod Menu", "Gun spawned from existing tool!", "Nice")
                    return true
                end
            end
            
            notify("Coño Mod Menu", "No gun template found!", "Okay")
            return false
        end
    end)
    
    if not success then
        notify("Coño Mod Menu", "Gun spawn failed: " .. tostring(error), "Okay")
        return false
    end
end

-- Menu Functions
local function createMainMenu()
    mainMenu = Instance.new("ScreenGui")
    mainMenu.Name = "CoñoModzMenu"
    mainMenu.Parent = game.CoreGui
    
    menuFrame = Instance.new("Frame")
    menuFrame.Size = UDim2.new(0, 500, 0, 130) -- Höher für zwei Reihen
    menuFrame.Position = UDim2.new(0.5, -250, 0.3, -40)
    menuFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    menuFrame.BorderSizePixel = 0
    menuFrame.Visible = false
    menuFrame.Active = true
    menuFrame.Draggable = true
    menuFrame.Parent = mainMenu
    
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 8)
    corner.Parent = menuFrame
    
    local title = Instance.new("TextLabel")
    title.Size = UDim2.new(1, 0, 0, 25)
    title.Position = UDim2.new(0, 0, 0, 0)
    title.BackgroundTransparency = 1
    title.Text = "Coño Mod Menu by Vox"
    title.TextColor3 = Color3.fromRGB(255, 255, 255)
    title.TextScaled = true
    title.Font = Enum.Font.SourceSansBold
    title.Parent = menuFrame
    
    local closeBtn = Instance.new("TextButton")
    closeBtn.Size = UDim2.new(0, 25, 0, 25)
    closeBtn.Position = UDim2.new(1, -27, 0, 2)
    closeBtn.BackgroundColor3 = Color3.fromRGB(60, 60, 60)
    closeBtn.Text = "X"
    closeBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    closeBtn.Font = Enum.Font.SourceSansBold
    closeBtn.TextScaled = true
    closeBtn.Parent = menuFrame
    
    local closeCorner = Instance.new("UICorner")
    closeCorner.CornerRadius = UDim.new(0, 4)
    closeCorner.Parent = closeBtn
    
    closeBtn.MouseButton1Click:Connect(function()
        menuFrame.Visible = false
        settings.menuVisible = false
    end)
    
    -- ESP Toggle Button (separate Variable für Farbsteuerung)
    local espToggleBtn = Instance.new("TextButton")
    espToggleBtn.Size = UDim2.new(0, 90, 0, 35)
    espToggleBtn.Position = UDim2.new(0, 10, 1, -85) -- Über der ersten Reihe
    espToggleBtn.BackgroundColor3 = Color3.fromRGB(60, 60, 60) -- Grau = Aus
    espToggleBtn.Text = "ESP: OFF"
    espToggleBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    espToggleBtn.TextScaled = true
    espToggleBtn.Font = Enum.Font.SourceSans
    espToggleBtn.Parent = menuFrame
    
    local espBtnCorner = Instance.new("UICorner")
    espBtnCorner.CornerRadius = UDim.new(0, 6)
    espBtnCorner.Parent = espToggleBtn
    
    -- ESP Toggle Funktion
    local function updateESPToggleButton()
        if settings.espEnabled then
            espToggleBtn.BackgroundColor3 = Color3.fromRGB(0, 170, 0) -- Grün = An
            espToggleBtn.Text = "ESP: ON"
        else
            espToggleBtn.BackgroundColor3 = Color3.fromRGB(60, 60, 60) -- Grau = Aus
            espToggleBtn.Text = "ESP: OFF"
        end
    end
    
    -- Initialen Zustand setzen
    updateESPToggleButton()
    
    espToggleBtn.MouseButton1Click:Connect(function()
        toggleESP()
        updateESPToggleButton()
    end)
    
    -- Hover effects für ESP Button
    espToggleBtn.MouseEnter:Connect(function()
        if settings.espEnabled then
            TweenService:Create(espToggleBtn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(0, 200, 0)}):Play()
        else
            TweenService:Create(espToggleBtn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(80, 80, 80)}):Play()
        end
    end)
    
    espToggleBtn.MouseLeave:Connect(function()
        updateESPToggleButton() -- Zurück zur richtigen Farbe
    end)
    
    -- Einfache einreihige Buttons (nur die wichtigsten)
    local buttons = {
        {text = "Spoof VC", func = spoofVoiceChat},
        {text = "Server Switch", func = serverSwitch},
        {text = "Anti AFK", func = toggleAntiAFK},
        {text = "Spawn Knife", func = spawnKnife},
        {text = "Spawn Gun", func = spawnGun} -- Neuer Button für Murder Gun
    }
    
    for i, btnData in ipairs(buttons) do
        local btn = Instance.new("TextButton")
        btn.Size = UDim2.new(0, 90, 0, 35) -- Kleinere Buttons für bessere Platzierung
        btn.Position = UDim2.new(0, 10 + (i-1) * 95, 1, -45) -- Zweite Reihe (unten)
        btn.BackgroundColor3 = Color3.fromRGB(60, 60, 60)
        btn.Text = btnData.text
        btn.TextColor3 = Color3.fromRGB(255, 255, 255)
        btn.TextScaled = true
        btn.Font = Enum.Font.SourceSans
        btn.Parent = menuFrame
        
        local btnCorner = Instance.new("UICorner")
        btnCorner.CornerRadius = UDim.new(0, 6)
        btnCorner.Parent = btn
        
        -- Hover effects
        btn.MouseEnter:Connect(function()
            TweenService:Create(btn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(80, 80, 80)}):Play()
        end)
        
        btn.MouseLeave:Connect(function()
            TweenService:Create(btn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(60, 60, 60)}):Play()
        end)
        
        btn.MouseButton1Click:Connect(function()
            -- Button click effect - turn black
            btn.BackgroundColor3 = Color3.fromRGB(0, 0, 0)
            wait(0.2)
            btn.BackgroundColor3 = Color3.fromRGB(60, 60, 60)
            
            btnData.func()
        end)
    end
    
    return mainMenu
end

local function toggleMenu()
    settings.menuVisible = not settings.menuVisible
    if menuFrame then
        menuFrame.Visible = settings.menuVisible
    end
end

-- UI Functions
local function createRainbowText()
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "CoñoModz"
    screenGui.Parent = game.CoreGui
    
    local textLabel = Instance.new("TextLabel")
    textLabel.Size = UDim2.new(0, 300, 0, 50)
    textLabel.Position = UDim2.new(0.5, -150, 0, 60) -- Further down
    textLabel.BackgroundTransparency = 1
    textLabel.Text = "Coño Modz - guns.lol/xup"
    textLabel.TextColor3 = Color3.fromRGB(255, 0, 0)
    textLabel.TextScaled = true
    textLabel.Font = Enum.Font.SourceSansBold
    textLabel.Parent = screenGui
    
    -- Rainbow effect
    spawn(function()
        while settings.rainbowTextEnabled do
            for hue = 0, 1, 0.01 do
                textLabel.TextColor3 = Color3.fromHSV(hue, 1, 1)
                wait(0.1)
            end
        end
    end)
    
    return screenGui
end

local function createKeybindsUI()
    keybindsGui = Instance.new("ScreenGui")
    keybindsGui.Name = "KeybindsUI"
    keybindsGui.Parent = game.CoreGui
    
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(0, 200, 0, 150)
    frame.Position = UDim2.new(1, -210, 0.5, -75)
    frame.BackgroundColor3 = Color3.fromRGB(0, 0, 0)
    frame.BackgroundTransparency = 0.3
    frame.BorderSizePixel = 0
    frame.Parent = keybindsGui
    
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 8)
    corner.Parent = frame
    
    local title = Instance.new("TextLabel")
    title.Size = UDim2.new(1, 0, 0, 25)
    title.Position = UDim2.new(0, 0, 0, 0)
    title.BackgroundTransparency = 1
    title.Text = "Keybinds"
    title.TextColor3 = Color3.fromRGB(255, 255, 255)
    title.TextScaled = true
    title.Font = Enum.Font.SourceSansBold
    title.Parent = frame
    
    local keybinds = {
        "F1 = NoClip", 
        "F2 = Kill Sheriff",
        "F3 = Attach to Sheriff",
        "F4 = Spoof VC",
        "INSERT = Menu"
    }
    
    for i, text in ipairs(keybinds) do
        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(1, -10, 0, 20)
        label.Position = UDim2.new(0, 5, 0, 25 + (i-1) * 20)
        label.BackgroundTransparency = 1
        label.Text = text
        label.TextColor3 = Color3.fromRGB(200, 200, 200)
        label.TextScaled = true
        label.Font = Enum.Font.SourceSans
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.Parent = frame
    end
    
    return keybindsGui
end

-- Keybind Handler
UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end
    
    if input.KeyCode == Enum.KeyCode.F1 then
        toggleNoClip()
    elseif input.KeyCode == Enum.KeyCode.F2 then
        killSheriff()
    elseif input.KeyCode == Enum.KeyCode.F3 then
        attachToSheriff()
    elseif input.KeyCode == Enum.KeyCode.F4 then
        spoofVoiceChat()
    elseif input.KeyCode == Enum.KeyCode.Insert then
        toggleMenu()
    end
end)

-- ESP Handler für neue Spieler (nur wenn ESP aktiv)
Players.PlayerAdded:Connect(function(player)
    if player ~= LocalPlayer and settings.espEnabled then
        player.CharacterAdded:Connect(function()
            wait(0.5)
            createESP(player)
        end)
    end
end)

-- Initialize
local function init()
    -- Show load notification
    StarterGui:SetCore("SendNotification", {
        Title = "Coño Mod Menu by Vox",
        Text = "guns.lol/xup",
        Duration = 5,
        Button1 = "Okay Daddy"
    })
    
    -- Create UI
    createRainbowText()
    createKeybindsUI()
    createMainMenu()
    
    -- Wait for character
    LocalPlayer.CharacterAdded:Connect(function(character)
        wait(1)
        if settings.espEnabled then
            for _, player in pairs(Players:GetPlayers()) do
                if player ~= LocalPlayer then
                    createESP(player)
                end
            end
        end
    end)
    
    -- **WICHTIG: Stelle sicher, dass ESP beim Start ausgeschaltet ist**
    -- Entferne alle bestehenden ESP-Elemente
    removeESP()
    settings.espEnabled = false
end

-- Start the script
init()

