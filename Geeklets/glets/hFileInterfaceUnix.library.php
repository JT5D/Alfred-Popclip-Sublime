<html><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8"></head><body><pre>&lt;?php

//\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//\\\       \\\\\\\\|
//\\\ @@    @@\\\\\\| Hot Toddy File Unix Interface
//\\ @@@@  @@@@\\\\\|
//\\\@@@@| @@@@\\\\\|
//\\\ @@ |\\@@\\\\\\| http://www.hframework.com
//\\\\  ||   \\\\\\\| © Copyright 2012 Richard York, All rights Reserved
//\\\\  \\_   \\\\\\|
//\\\\\        \\\\\| Use and redistribution are subject to the terms of the license.
//\\\\\  ----  \@@@@| http://www.hframework.com/license
//@@@@@\       \@@@@|
//@@@@@@\     \@@@@@|
//\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class hFileInterfaceUnixLibrary extends hFileInterface {

    private $hFileSpotlightMD;

    public $filterPaths = array();
    public $fileTypes = array();

    private $labels = array(
        'none',
        'gray',
        'green',
        'purple',
        'blue',
        'yellow',
        'red',
        'orange'
    );
    
    public $methodsWereAdded = false;
    
    public function hConstructor()
    {

    }
    
    public function shouldBeCalled()
    {
        return $this-&gt;isServerPath;
    }
    
    public function getMethods()
    {
        // Can't use something nice and simple like get_class_methods(), 
        // it returns all methods from all parent objects, and I only want
        // this to return the methods from this object only.
        return array(
            'shouldBeCalled',
            'getMIMEType',
            'getTitle',
            'upload',
            'getSize',
            'getDescription',
            'getMetaData',
            'getLastModified',
            'getCreated',
            'hasChildren',
            'getDirectories',
            'getFiles',
            'getLabel',
            'rename',
            'delete',
            'newDirectory'
        );
    }

    // Create a new interface for Mac using the mdls command
    public function getMIMEType()
    {
        return $this-&gt;isDirectory? 'Directory' : $GLOBALS['hFramework']-&gt;getMIMEType($this-&gt;serverPath);
    }

    public function getTitle()
    {
        return '';
    }

    public function upload($hFiles)
    {
        $response = 1;
        
        // Path is the directory we're uploading to.... 
        foreach ($hFiles as $i =&gt; $hFile)
        {
            // Get rid of nefarious characters
            $hFile['hFileName'] = str_replace(
                array(
                    "\t", '@', "\n", ':', "\\", "/", '(', ')', '[', ']', '{', '}', 
                    '&amp;', '$', '#', '!', '*', '^', '%', '+', '-', '=', '~', '`', 
                    '?', '&lt;', '&gt;', '"', '\'', '|', ';'
                ),
                '',
                trim($hFile['hFileName'])
            );
            
            // Cut out excessive spacing within the file name
            if (strstr($hFile['hFileName'], '  '))
            {
                while (strstr($hFile['hFileName'], '  '))
                {
                    $hFile['hFileName'] = str_replace('  ', ' ', $hFile['hFileName']);
                }
            }
 
            $savePath = $this-&gt;getConcatenatedPath($this-&gt;serverPath, $hFile['hFileName']);

            if (file_exists($savePath))
            {
                $hFile['hFileId'] = $this-&gt;fileId;

                if ($hFile['hFileReplace'])
                {
                    $GLOBALS['hFramework']-&gt;move($hFile['hFileTempPath'], $savePath);
                }
                else
                {
                    $response = 0;
                }
            }
            else
            {
                $GLOBALS['hFramework']-&gt;move($hFile['hFileTempPath'], $savePath);
            }
        }

        return $response;
    }

    public function getDescription()
    {
        return $this-&gt;command('file -b '.escapeshellarg($this-&gt;serverPath));
    }

    public function getMetaData()
    {
        if ($this-&gt;hOS == 'Darwin')
        {
            $this-&gt;hFileSpotlightMD = $this-&gt;library('hFile/hFileSpotlight/hFileSpotlightMD');
            return $this-&gt;hFileSpotlightMD-&gt;get($this-&gt;serverPath);
        }
        
        return array();
    }

    public function getSize()
    {
        return $this-&gt;isDirectory?
                $this-&gt;bytes((int) $this-&gt;command('du -sx '.escapeshellarg($this-&gt;serverPath)))
            :
                $this-&gt;bytes(@filesize($this-&gt;serverPath));
    }

    public function getLastModified()
    {
        return @filemtime($this-&gt;serverPath);
    }

    public function getCreated()
    {
        return @filectime($this-&gt;serverPath);
    }

    public function hasChildren($countFiles = false)
    {
        if ($this-&gt;exists &amp;&amp; $this-&gt;isDirectory)
        {
            if (false !== ($dh = @opendir($this-&gt;serverPath)))
            {
                while (false !== ($file = readdir($dh)))
                {
                    $server_path = $this-&gt;getConcatenatedPath($this-&gt;serverPath, $file);

                    $type = @filetype($server_path);

                    if ($file != '.' &amp;&amp; $file != '..' &amp;&amp; substr($file, 0, 1) != '.' &amp;&amp; $type == 'dir' || $countFiles &amp;&amp; $type == 'file' &amp;&amp; $file != '.DS_Store')
                    {
                        closedir($dh);
                        return true;
                    }
                }

                closedir($dh);
            }
        }

        return false;
    }

    public function getDirectories()
    {
        $directories = array();

        if ($this-&gt;exists &amp;&amp; $this-&gt;isDirectory)
        {
            if (false !== ($dh = @opendir($this-&gt;serverPath)))
            {
                while (false !== ($file = readdir($dh)))
                {
                    $serverPath = $this-&gt;getConcatenatedPath($this-&gt;serverPath, $file);

                    $type = @filetype($serverPath);

                    if ($file != '.' &amp;&amp; $file != '..' &amp;&amp; ($type == 'dir' || $type == 'link') &amp;&amp; $file != '.DS_Store')
                    {
                        $virtualPath = $this-&gt;getVirtualFileSystemPath($serverPath);
                    
                        $properties = array(
                            'hFileInterfaceObjectId'  =&gt; $serverPath,
                            'hFileName'               =&gt; $file,
                            'hFilePath'               =&gt; $virtualPath,
                            'hFileIsServer'           =&gt; true,
                            'hDirectoryId'            =&gt; str_replace('=', '', base64_encode($serverPath)).'s',
                            'hDirectoryIsApplication' =&gt; false,
                            'hFileIconId'             =&gt; 0,
                            'hFileCreated'            =&gt; @filectime($serverPath),
                            'hFileLastModified'       =&gt; @filemtime($serverPath),
                            'hFileDescription'        =&gt; '',
                            'hFileMIME'               =&gt; 'directory',
                            'hFileCount'              =&gt; $this-&gt;hasChildren(true),
                            'hDirectoryCount'         =&gt; $this-&gt;hasChildren()
                        );
 
                        if ($this-&gt;hOS == 'Darwin')
                        {
                            $meta = $this-&gt;hFile-&gt;getMetaData($virtualPath);
                            
                            $label = 0;
                            
                            if (isset($meta['kMDItemFSLabel']))
                            {
                                $label = (int) $meta['kMDItemFSLabel'];
                            }
                            else if (isset($meta['FSLabel']))
                            {
                                $label = (int) $meta['FSLabel'];
                            }

                            $properties['hFileLabel'] = $this-&gt;labels[$label];
                        }
                        
                        $directories[$file] = $properties;
                    }
                }

                closedir($dh);
            }
            else
            {
                return 403;
            }
        }

        return $directories;
    }

    public function getFiles()
    {
        $files = array();

        if ($this-&gt;exists($this-&gt;filePath))
        {
            if (false !== ($dh = @opendir($this-&gt;serverPath)))
            {
                while (false !== ($file = readdir($dh)))
                {
                    $serverPath = $this-&gt;getConcatenatedPath($this-&gt;serverPath, $file);

                    if ($file != '.' &amp;&amp; $file != '..' &amp;&amp; @filetype($serverPath) == 'file' &amp;&amp; $file != '.DS_Store')
                    {
                        $virtualPath = $this-&gt;getVirtualFileSystemPath($serverPath);

                        $properties = $this-&gt;getFileProperties($virtualPath);

                        if ($this-&gt;hOS == 'Darwin')
                        {
                            $meta = $this-&gt;hFile-&gt;getMetaData($virtualPath);
                            
                            $label = 0;
                            
                            if (isset($meta['kMDItemFSLabel']))
                            {
                                $label = (int) $meta['kMDItemFSLabel'];
                            }
                            else if (isset($meta['FSLabel']))
                            {
                                $label = (int) $meta['FSLabel'];
                            }
                            
                            $properties['hFileInterfaceObjectId'] = $serverPath;
                            $properties['hFileLabel'] = $this-&gt;labels[$label];
                        }
                    
                        $files[$file] = $properties;
                    }
                }

                closedir($dh);
            }
            else
            {
                return 403;
            }
        }

        return $files;
    }
    
    public function getLabel()
    {
        if ($this-&gt;hOS == 'Darwin')
        {
            $meta = $this-&gt;getMetaData();
            
            $label = 0;

            if (isset($meta['kMDItemFSLabel']))
            {
                $label = (int) $meta['kMDItemFSLabel'];
            }
            else if (isset($meta['FSLabel']))
            {
                $label = (int) $meta['FSLabel'];
            }

            return $this-&gt;labels[$label];
        }
        
        return 'none';
    }

    public function rename($newName)
    {
        // Remember the old path
        $newPath = $this-&gt;getConcatenatedPath($this-&gt;parentDirectoryPath, $newName);

        // Next step is see if the "renamed" direcory or file already exists.
        // Circumvent namespace clashing in the VFS
        // See if a directory exists, if directory
        // See if a file exists, if file
        if ($this-&gt;exists($newPath))
        {
            $rtn = -3;
        }
        else
        {
            $GLOBALS['hFramework']-&gt;move($this-&gt;serverPath, $this-&gt;getServerFileSystemPath($newPath));
            $rtn = 1;
        }

        return $rtn;
    }

    public function delete()
    {
        return $this-&gt;rm($this-&gt;serverPath, !$this-&gt;isDirectory);
    }

    public function newDirectory($newDirectoryName, $hUserId = 0)
    {
        $path = $this-&gt;getConcatenatedPath($this-&gt;serverPath, $newDirectoryName);

        if (!file_exists($path))
        {
            mkdir($path);
            return str_replace('=', '', base64_encode($path)).'s';
        }
        else
        {
            return -3;
        }
    }
}

?&gt;</pre></body></html>