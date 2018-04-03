<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class SkylineController extends Controller
{
    public function main() {
    	$process = new Process("py ReverseSkylineIncompleteData.py");
    	$process->run();

    	if(!$process->isSuccessful()) {
    		throw new ProcessFailedException($process);
    	}

    	echo $process->getOutput();
    }

    public function index() {
    	return view('index');
    }
}
