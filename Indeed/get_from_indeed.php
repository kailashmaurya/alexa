<?
define("INDEED_API","http://api.indeed.com/ads/apisearch?v=2&publisher={your_publisher_id}d&q=");
if(isset($_GET['job'])){
    $job = $_GET['job'];
    $location = $_GET['location'];
    
    //get results from Indeed
    $fileContents = file_get_contents(INDEED_API.urlencode($job)."&l=".urlencode($location)."&sort=&radius=&st=&jt=&start=&limit=&fromage=&filter=&co=us&chnl=");
    
    //convert xml to json
    $fileContents = str_replace(array("\n", "\r", "\t"), '', $fileContents);
    $fileContents = trim(str_replace('"', "'", $fileContents));
    $simpleXml = simplexml_load_string($fileContents);
    $json = json_encode($simpleXml);
    
    //construct email body
    $obj = json_decode($json);
    $mailbody = "";
    if($obj->totalresults!='0'){
        $arr = $obj->results;
        $arr = $arr->result;
        foreach( $arr as $a_job ) {
            $mailbody = $mailbody."\n\n".$a_job->jobtitle." : ".$a_job->company." : ".$a_job->url;
        }
        
        //send search results email
        $command = "echo '".$mailbody."' | mailx -s 'Alexa Search Result : ".$job.", ".$location."' {recepient_email_id}";
        exec($command);
        
        //prepare json response
        $count = count($obj->results->result);
        $response = array("success"=>true, "count"=>(string)$count);
        echo json_encode($response);
    }
    else{
        //return no results response
        $response = array("success"=>false, "count"=>'0');
        echo json_encode($response);
    }
}
?>