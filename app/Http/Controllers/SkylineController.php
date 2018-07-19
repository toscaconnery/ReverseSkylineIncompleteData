<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Http\Requests;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class SkylineController extends Controller
{
    public function main() {
    	$process = new Process("py script.py");
    	$process->run();

    	if(!$process->isSuccessful()) {
    		throw new ProcessFailedException($process);
    	}

    	echo $process->getOutput();
    }

    public function index() {
    	return view('index');
    }

    public function runbasic() {
        $process = new Process("py scriptx.py");
        $process->run();

        if(!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        #echo $process->getOutput();
        $hasil = $process->getOutput();
        #dd("done this");
        return view('DirectResult', compact('hasil'));
    }

    public function testOutPut(){
        $process = new Process("py live_skyline.py");
        $process->run();

        if(!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        #echo $process->getOutput();
        $hasil = $process->getOutput();
        #dd("done this");
        return view('DirectResult', compact('hasil')); 
    }

    public function showForm(){
        return view('ShowForm');
    }

    public function post_input(Request $request){
        $perintah = "py input_skyline.py";
        $query_point = $request->query_point;
        $data_point = $request->data_point;
        $perintah = $perintah." $query_point $data_point";
        // dd($perintah);

        $process = new Process($perintah);
        $process->run();

        if(!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        $hasil = $process->getOutput();

        return view('DirectResult', compact('hasil'));
    }
}
