<?php
	
	// grab user input if present (optional)
	$comm = $argv[1];

	// display the about info for this extension
	if ($comm == "about") {

		echo "Extension Updater is an extension created by David Ferguson (@jdfwarrior) that makes it easy to update your Alfred extensions. This extension will scan Alfred for supporting extensions, and then check for updates. If an update is available, the update will automatically download and install.";
		exit(1);
		
	} // end if about

	// display the version info for this extension
	else if ($comm == "version") {
			
		// if update.xml exists, display version info
		if (file_exists("update.xml")) {
			$xml = simplexml_load_file("update.xml");
			echo "Extension Updater $xml->version";
		}

		// if update.xml doesn't exist, show an error
		else {
			echo "No version information found for this extension";
		}

		exit(1);

	} // end else version

	// display the changelog for this extension
	else if ($comm == "changelog") {
		
		// if changelog exists, show contents
		if (file_exists("changelog.txt")) {

			$f = fopen("changelog.txt", "r");
			while ($output = fgets($f)) {
				echo $output."\r";
			}
			fclose($f);

		}

		// if changelog doesn't exist, display error
		else {
			echo "No changelog found.";
		}
		exit(1);

	} // end else changelog

	// display help menu to user
	else if ($comm == "help") {
		
		echo "¬ update check - Check for available updates\r";
		echo "¬ update - Update all available extensions\r";
		echo "¬ update about - About extension\r";
		echo "¬ update version - Extension version\r";
		echo "¬ update changelog - Display changelog\r";
		echo "¬ update help - Display help menu\r";
		exit(1);	
		
	} //end else help

	// Get the current directory
	$cd = getcwd();
	
	// Split the full path into an array so that the current folder can be removed
	// returning the parent folder.
	$path = explode("/", $cd);

	// Count the number of elements in the full path so that the current folder can be removed
	// and return only the parent
	$size = count($path);
	$size--;
	unset($path[$size]);

	// Glue the full path back together
	$path = implode("/", $path);

	// Get a list of all items in the folder
	$dirs = scandir($path);
	$inc = 0;

	// Remove items that aren't of interest
	foreach($dirs as $dir):

		if (!is_dir($path."/".$dir) || $dir == "." || $dir == "..") { unset($dirs[$inc]); }
		$inc++;

	endforeach;

	$updates = false;


	// Extension Update
	// 1. Search through each script directory searching for an update.xml
	// 2. If an update.xml is available, read the current version and remote xml path.
	// 3. Check remote xml verion against local
	// 4. If a new version is available, read remote xml update url
	// 5. Download updated extension
	// 6. Unzip extension
	foreach($dirs as $dir):

		// Check for the existence of update.xml in the path
		if (file_exists($path."/".$dir."/"."update.xml")) {

			// Read the local version and update url for the extension
			$lxml 	  = simplexml_load_file($path."/".$dir."/"."update.xml");
			$lversion = floatval($lxml->version);
			$lurl 	  = $lxml->url;

			// Read the remote version and update url for the extension}
			$rxml 	  = @simplexml_load_file($lurl);
			
			if ($rxml != false) {
				
				$rversion = floatval($rxml->version);
				$rurl 	  = $rxml->url;

				// If a new version exists, update
				if ($lversion < $rversion) {
					
					// Set flag indicating that updates were found and then save
					// remote filename
					$updates = true;
					$file = basename($rurl);

					if ($comm != "check") {
						
						// Download the remote file via cURL then unzip and remove the
						// newly downloaded extension
						exec("curl \"$rurl\" > \"$path/$dir/$file\"");
						if (file_exists("$path/$dir/$file")) {
						
							str_replace("%20", " ", $file);
							exec("unzip -o  \"$path/$dir/$file\" -d \"$path/$dir/\"");
							exec("rm \"$path/$dir/$file\"");

						}

						// Inforom the user that the extension was updated
						$lxml 	  = simplexml_load_file($path."/".$dir."/"."update.xml");
						$lversion = floatval($lxml->version);
						if ($lversion == $rversion) {
							echo "Updated $dir\r";
						}
						else {
							echo "Error updating $dir from $lversion to $rversion\r";
						}
					}

					else if ($comm == "check") {
						
						echo "¬ $dir $rversion is available.\r";
						if (isset($rxml->comments)) {
							echo $rxml->comments."\r";
						}

					}

				}

			}

		}
	endforeach;

	// If no updates were found, inform the user
	if (!$updates) { echo "No updates available"; }

?>