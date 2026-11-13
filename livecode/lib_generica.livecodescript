script "lib_generica"
######################################################################################
## LIB_GENERICA  (13 11 2026)
## A game's words as plain label files: retheme a game by editing labels, not code.
## sets/<theme>/<category>/<list>.txt = a '#' header, then one label per line (in order).
## A theme can sit on a base theme: lists it doesn't have come from the base, so a
## retheme holds only what changes. Engine-free: use it as a library (start using).
##   Gen.Load setsFolder, theme [, baseTheme]   load (base first, then the theme over it)
##   Gen.Label(list, n)       label n of a list (1-based)
##   Gen.List(list)           every label of a list, one per line
##   Gen.Count(list)          how many labels      Gen.About(list)   its description
##   Gen.Lists()              every list name       Gen.Theme()       the loaded theme
##   Gen.Fill(text, slots)    fill the slots of a label: slots["%"], slots["#"], slots["*"],
##                            slots["^0"], slots["^1"] ... (Galactica's markers)
##   Gen.Say(list, n, slots)  = Gen.Fill(Gen.Label(list, n), slots)
## Python twin: python/generica.py (same names, same files).
######################################################################################

local sLabels     -- [list] = labels, cr between
local sAbout      -- [list] = description
local sTheme

on Gen.Load pFolder, pTheme, pBase
   replace "\" with "/" in pFolder
   if char -1 of pFolder is "/" then delete char -1 of pFolder
   put empty into sLabels
   put empty into sAbout
   if pBase is not empty and pBase is not pTheme then Gen.LoadTheme pFolder & "/" & pBase
   Gen.LoadTheme pFolder & "/" & pTheme
   put pTheme into sTheme
   return the number of lines of the keys of sLabels
end Gen.Load

-- every <category>/<list>.txt under a theme folder (a list read later replaces one read earlier)
on Gen.LoadTheme pThemeFolder
   local tCat, tFile, tText, tName, tHead, tLine
   if there is not a folder pThemeFolder then return "no theme folder" && pThemeFolder
   repeat for each line tCat in folders(pThemeFolder)
      if tCat is "." or tCat is ".." then next repeat
      repeat for each line tFile in files(pThemeFolder & "/" & tCat)
         if char -4 to -1 of tFile is not ".txt" then next repeat
         put char 1 to -5 of tFile into tName
         put URL ("file:" & pThemeFolder & "/" & tCat & "/" & tFile) into tText
         replace numToChar(13) with empty in tText
         put empty into tHead
         repeat while char 1 of line 1 of tText is "#"
            put line 1 of tText into tLine
            if tLine begins with "# about:" then put word 3 to -1 of tLine into sAbout[tName]
            delete line 1 of tText
         end repeat
         if char -1 of tText is cr then delete char -1 of tText
         put tText into sLabels[tName]
      end repeat
   end repeat
   return empty
end Gen.LoadTheme

function Gen.Label pList, pN
   if pN is not a number then return empty
   return line pN of sLabels[pList]
end Gen.Label

function Gen.List pList
   return sLabels[pList]
end Gen.List

function Gen.Count pList
   if sLabels[pList] is empty then return 0
   return the number of lines of sLabels[pList]
end Gen.Count

function Gen.About pList
   return sAbout[pList]
end Gen.About

function Gen.Lists
   local tKeys
   put the keys of sLabels into tKeys
   sort lines of tKeys
   return tKeys
end Gen.Lists

function Gen.Theme
   return sTheme
end Gen.Theme

-- Galactica's slot markers: % # * and ^0 ^1 ... (longest markers first, so ^10 before ^1)
function Gen.Fill pText, pSlots
   local tKeys, tKey
   if pSlots is not an array then return pText
   put the keys of pSlots into tKeys
   sort lines of tKeys descending numeric by the number of chars of each
   repeat for each line tKey in tKeys
      replace tKey with pSlots[tKey] in pText
   end repeat
   return pText
end Gen.Fill

function Gen.Say pList, pN, pSlots
   return Gen.Fill(Gen.Label(pList, pN), pSlots)
end Gen.Say
