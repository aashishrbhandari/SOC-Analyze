
let ipList = [];

function addToIPList(ip_addr_list) {
    for (let ip_addr of ip_addr_list) {
        ipList.indexOf(ip_addr) === -1 ? ipList.push(ip_addr) : console.log("[-] Duplicate IP: ", ip_addr);
    }
}

function formatResultData(resultdata) {
    bl_list = []
    blacklisted_timeout = []
    blacklisted_exception = []

    for (one_bs of resultdata.bl_list) {
        bl_list.push(one_bs.dnsbl_name);
    }

    for (one_bs_timedout of resultdata.bl_timedout) {
        blacklisted_timeout.push(one_bs_timedout.dnsbl_name);
    }

    for (one_bs_exception of resultdata.bl_exception) {
        blacklisted_exception.push(one_bs_exception.dnsbl_name);
    }

    return new BlacklistedIP(resultdata.ip, resultdata.bl_count, bl_list, blacklisted_timeout, blacklisted_exception);
}

function buildErrorData(ip, errorStr) {
    bl_list = [errorStr, "Check Console", "Also check API Service"]
    blacklisted_timeout = []
    blacklisted_exception = [errorStr]
    return new BlacklistedIP(ip, 0, bl_list, blacklisted_timeout, blacklisted_exception);
}

function alertForIP_Data() {
    document.querySelector(".ip-list-show-card").innerHTML = `
        <div class="p-4 rounded border border-danger text-danger">
            No Data Selected... Please select Raw Strings or File
        </div>
    `;
}

function createIP_Header() {
    document.querySelector(".ip-list-show-card").innerHTML = `
        <div class="card-body border rounded mb-2">
            <select id="select-dns-timeout" class="form-select mb-2" aria-label="Default select example" style="width: 120px; height: 40px;">
                <option value="1">Default</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
            </select>
            <button class="btn btn-dark check-default-ip-bl">Check</button>
            <button class="btn btn-outline-dark clear-default-ip-bl">Clear</button>
        </div>
        <ul class="list-group ip-list-show-list">
        </ul>
    `;

    document.querySelector(".check-default-ip-bl").addEventListener('click', () => {
        // createHeader

        let rtimeout = document.querySelector("#select-dns-timeout").value;

        document.querySelector(".blkip-list-show-card").innerHTML = `
            <div class="card-body border rounded mb-2">
                Processing DNS BL Check with Timeout: ${rtimeout}
            </div>
            <div class="list-group mx-0 blkip-list-show-list"></div>
        `

        for (let oneip2check of ipList) {
            fetch(`http://192.168.1.6:5000/check_blacklist?ip=${oneip2check}&rtimeout=${rtimeout}`)
                .then(resultdata => resultdata.json())
                .then(resultdata => {
                    formattedResultData = formatResultData(resultdata);
                    document.querySelector(".blkip-list-show-list").insertAdjacentHTML("beforeend", create_BlacklistedIP_Status(formattedResultData));
                })
                .catch((error) => {
                    formattedResultData = buildErrorData(oneip2check, error);
                    document.querySelector(".blkip-list-show-list").insertAdjacentHTML("beforeend", create_BlacklistedIP_Status(formattedResultData));
                });
            ;
        }

    });

    document.querySelector(".clear-default-ip-bl").addEventListener("click", () => {
        clearIP_Header();
        ipList = "";
        document.querySelector(".blkip-list-show-card").innerHTML = ``;
    });

}

function clearIP_Header() {
    document.querySelector(".ip-list-show-card").innerHTML = `
        <div class="p-4 border rounded">
            No Data Selected & Processed    
        </div>
    `;
}

class BlacklistedIP {
    constructor(ip, blacklist_service_count, blacklisted, blacklisted_timeout, blacklisted_exception) {
        this.ip = ip;
        this.blacklist_service_count = blacklist_service_count;
        this.blacklisted = blacklisted;
        this.blacklisted_timeout = blacklisted_timeout;
        this.blacklisted_exception = blacklisted_exception;
    }
}

function createBadgeList(dataList) {
    badgerList = "";
    for (one_dataList of dataList) {
        badgerList += `<span class="badge bg-dark fs-6"> ${one_dataList} </span>`;
    }
    return badgerList;
}

function create_BlacklistedIP_Status(blacklistedIP) {
    return `
    <label class="list-group-item d-flex gap-2 border rounded-2 mb-2">
        <input class="form-check-input flex-shrink-0" type="checkbox" value="">
        <div class="bl-details w-100">
            
            <div class="d-flex justify-content-between mb-1">
                <div class="bl-ip fs-5 text-muted">${blacklistedIP.ip}</div>
                <div class="bl-status d-flex justify-content-center align-items-center gap-2">
                    <span class="badge bg-light text-dark border border-3 rounded-pill d-flex justify-content-center align-items-center gap-1">
                        <img src="img/danger1.png" width="14" height="14" class="mr-2" alt="">
                        <text>${blacklistedIP.blacklisted.length} </text>
                    </span>
                    <span class="badge bg-light text-dark border border-3 rounded-pill d-flex justify-content-center align-items-center gap-1">
                        <img src="img/warning1.png" width="14" height="14" class="mr-2" alt="">
                        <text>${blacklistedIP.blacklisted_timeout.length}</text>
                    </span>
                    <span class="badge bg-light text-dark border border-3 rounded-pill d-flex justify-content-center align-items-center gap-1">
                        <img src="img/exception1.png" width="14" height="14" class="mr-2" alt="">
                        <text>${blacklistedIP.blacklisted_exception.length}</text>
                    </span>
                    <span class="badge bg-light text-dark border border-3 rounded-pill d-flex justify-content-center align-items-center gap-1">
                        <img src="img/sum1.png" width="14" height="14" class="mr-2" alt="">
                        <text>${blacklistedIP.blacklist_service_count}</text>
                    </span>
                </div>
            </div>
            
            <small class="d-block text-muted bl-name d-flex flex-wrap gap-2">
                ${createBadgeList(blacklistedIP.blacklisted)}
            </small>
            
        </div>
    </label>
    `;

}


// Example POST method implementation:
async function fetchFromServer(url = '') {
    const response = await fetch(url);
    return response.json();
}

function create_IP_List(ip_data) {

    let ipLi = "";
    console.log("ip_data: inside create_IP_List: ", ip_data);
    for (let oneIP of ip_data) {
        ipLi += `<li class="list-group-item">${oneIP}</li>`;
    }

    return ipLi;
}


// Func uses Regular expression to check if string is a IP address [Return True or False based on Regex Match]
function checkIfValidIP(str) {
    const regexExp = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/gi;
    return regexExp.test(str);
}

// Fetches the Proper Seperator for File and Text data
function getSeperator(string_val) {
    let seperatorString = string_val

    if (seperatorString === "newline" || seperatorString === "") {
        seperatorString = "\n"; // Default
    }

    return seperatorString;
}


// Comments : Func Formats & Validated IP List (Also Checks for Duplicates) [Return Refined IP List]
function formatValidateIP(rawtextList) {
    let validatedIP = []
    for (one_rawtextList of rawtextList) {
        if (checkIfValidIP(one_rawtextList)) {
            validatedIP.indexOf(one_rawtextList) === -1 ? validatedIP.push(one_rawtextList) : console.log("[-] Duplicate IP: ", one_rawtextList);
        }
    }
    console.log("[+] Valid IP List: ", validatedIP);
    return validatedIP;
}



// Comments: Process Text File Data
function process_txt_data(seperator, rawtextdata) {

    let seperatorString = getSeperator(seperator);
    let rawtextList = rawtextdata.split(seperatorString);
    addToIPList(formatValidateIP(rawtextList));
    console.log("iplist: ", ipList);

    if (ipList.length > 0) {
        let ipList_html = create_IP_List(ipList);
        document.querySelector(".ip-list-show-list").insertAdjacentHTML("beforeend", ipList_html);
    }
}

function process_file_data(seperator, selectedfile) {
    let reader = new FileReader();
    reader.onload = function (event) {
        let filetextData = event.target.result;
        let seperatorString = getSeperator(seperator);
        let rawtextList = filetextData.split(seperatorString);
        addToIPList(formatValidateIP(rawtextList));
        console.log("iplist: ", ipList);

        if (ipList.length > 0) {
            let ipList_html = create_IP_List(ipList);
            document.querySelector(".ip-list-show-list").insertAdjacentHTML("beforeend", ipList_html);
        }

    }
    reader.readAsText(selectedfile);
}

function process_file_and_text_data(seperator, selectedfile, rawtextdata) {

    let reader = new FileReader();
    reader.onload = function (event) {
        let filetextData = event.target.result;
        let seperatorString = getSeperator(seperator);

        let rawtextList = filetextData.split(seperatorString);
        addToIPList(formatValidateIP(rawtextList));

        let rawtextList2 = rawtextdata.split(seperatorString);
        addToIPList(formatValidateIP(rawtextList2));

        console.log("iplist: ", ipList);

        if (ipList.length > 0) {
            let ipList_html = create_IP_List(ipList);
            document.querySelector(".ip-list-show-list").insertAdjacentHTML("beforeend", ipList_html);
        }

    }
    reader.readAsText(selectedfile);
}

document.querySelector(".process-data").addEventListener("click", () => {
    ipList = [];
    clearIP_Header();


    let seperator = document.querySelector("#inputSeperator").value;
    let selectedfile = document.querySelector("#inputFile").files[0];
    let rawtextdata = document.querySelector("#inputTextArea").value;

    if (selectedfile) {
        createIP_Header();
        process_file_and_text_data(seperator, selectedfile, rawtextdata);
    } else {
        if (rawtextdata.trim() !== "") {
            createIP_Header();
            process_txt_data(seperator, rawtextdata)
        } else {
            alertForIP_Data();
        }
    }

});


















/* Code
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

counter = 1;


document.querySelector(".btn-test-tooltip").addEventListener('click', () => {
    document.querySelector(".blkip-list-show-card").innerHTML += `<button type="button" class="btn btn-secondary btn-test-tooltip" data-bs-toggle="tooltip" data-bs-placement="top" title="Tooltip on top">
        Tooltip on C:${counter}
    </button>`;
    counter++;
});

*/