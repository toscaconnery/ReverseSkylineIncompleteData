<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class TestController extends Controller
{
    public function testPython() {
    	$text = "abcdefghijklmn";
    	$process = new Process("py testPython.py");
    	$process->run();

    	if(!$process->isSuccessful()) {
    		throw new ProcessFailedException($process);
    	}

    	echo $process->getOutput();
    	dd("bisa");
    }
}
