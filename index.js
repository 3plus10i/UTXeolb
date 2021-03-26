class CommentSet {
    // 芦苇岛的文本导出格式
    pat_title_weed = /(?<id>\w{7}) \d{4}-\d{2}-\d{2}\([一|二|三|四|五|六|日]\)\d{2}:\d{2}:\d{2} No.(?<no>\d+)/;
    // PC网页的格式
    pat_title_pc = /20\d\d-\d\d-\d\d\([一|二|三|四|五|六|日]\)\d{2}:\d{2}:\d{2} ID:(?<id>\w{7})\s(?<po>\(PO主\))?.+No.(?<no>\d+)/;

    constructor(comments) {
        this.comments = comments.split('\n');
        this.ids = [];
        this.nos = [];

        this.headshot = null; // headshot:int 首个有效位为n时直接结束计点
        this.startn = 1; // startn:int 从n楼开始计算
        this.lastn = 1; // lastn:int 取倒数第n个位数
        this.block_po = true; // block_po:ToF 屏蔽po主的roll点
        this.blackIdList = []; // blackIdList:Array po主饼干
        this.block_visited = true; // block_visited:ToF 屏蔽重复饼干的roll点

        this.silent = false; // silent:ToF 禁止向console输出

    }

    parse() {
        // 从原始文本解析出【所有】id&no
        // 在pc输入时还会自动解析添加poid
        let matchResult, line;
        for (let i = 0; i < this.comments.length; i++) {
            line = this.comments[i];
            matchResult = line.match(this.pat_title_weed);
            if (matchResult != null) {
                this.ids.push(matchResult.groups['id']);
                this.nos.push(matchResult.groups['no']);
            }
        }
        // 当pat_title_weed匹配不到任何结果时，尝试PC模式
        if(this.ids.length==0){
            for (let i = 0; i < this.comments.length; i++) {
                line = this.comments[i];
                matchResult = line.match(this.pat_title_pc);
                if (matchResult != null) {
                    this.ids.push(matchResult.groups['id']);
                    this.nos.push(matchResult.groups['no']);
                    if(matchResult.groups['po'] && !this.blackIdList.includes(matchResult.groups['id'])){
                        this.blackIdList.push(matchResult.groups['id'])
                    }
                }

            }
        }
    }

    count_point() {
        // 计点

        let headshot = this.headshot;
        let startn = this.startn;
        let lastn = this.lastn;
        let silent = this.silent;
        let block_po = this.block_po;
        let blackIdList = block_po ? this.blackIdList : [];
        let block_visited = this.block_visited;

        const BLOCK = '已屏蔽';
        const DUPLICATED = '已roll';
        const SKIP = '不计入';
        const VALID = '有效  ';

        let report_list = [];
        let count = 0;
        let visited_ids = [];
        let summary = [];
        let head = ['id\t', 'No\t\t', 'status\t', 'sum'].join('');
        for (let i = 0; i < this.ids.length; i++) {
            let id = this.ids[i];
            let no = this.nos[i];
            if (blackIdList.includes(id)) {
                report_list.push([id, no, BLOCK, String(count)]);
                continue;
            }
            if (startn > 1) {
                startn -= 1;
                report_list.push([id, no, SKIP, String(count)]);
                continue;
            }
            if (block_visited && visited_ids.includes(id)) {
                report_list.push([id, no, DUPLICATED, String(count)]);
            }
            else {
                visited_ids.push(id);
                count += Number(no[no.length - lastn]);
                summary.push(no[no.length - lastn]);
                report_list.push([id, no, VALID, String(count)]);
                if (headshot != null & count == headshot) {
                    summary = 'headshot!';
                    break;
                }
                headshot = null;
            }
        }
        count = String(count);
        count = count[count.length - 1];

        // 所有有效点数5个一组分开
        if(summary.length == 0){
            summary = "什么都没统计到啊(*°-°)";
        }
        else{
            let summary_ = [];
            let i = 0;
            while (i + 4 < summary.length) {
                summary_.push(summary.slice(i, i + 5).join(''));
                i += 5;
            }
            summary_.push(summary.slice(i, summary.length).join(''));
            summary = summary_.join(' ');
        }
        

        // 报告
        let report = '';
        let abstract = '';
        report = report + summary + '\n';
        report = report + '目前点数：' + count + '\n';
        abstract = report;
        report = report + '=====以下为详细报告=====' + '\n';
        report = report + head + '\n';

        for (let i in report_list) {
            report = report + report_list[i].join('\t') + '\n';
        }
        if (!silent) {
            console.log(report);
        }
        return {"abstract": abstract, "report": report};
    }

}

function count_button(){
    // 获取输入文本
    let i = document.getElementById("in");
    let cs = new CommentSet(i.value);
    cs.parse();

    // 设置控制参数
    cs.lastn = parseInt(document.getElementById("lastn").value);
    cs.block_po = document.getElementById("block_po").checked;
    if(cs.blackIdList.length != 0){
        // 如果parse()后cs.blackIdList存在的话，说明解析出了(PO)，那就将表单的输入改为检测到的值
        document.getElementById("poid").value = cs.blackIdList.join(" ")
    }
    else{
        // 如果没解析出(PO)，那这里默认会是1pGvS00，这是由html里的硬编码默认值决定的。
        cs.blackIdList = document.getElementById("poid").value;
    }
    cs.block_visited = document.getElementById("block_visited").checked;
    

    // 计点
    let report = cs.count_point();

    // 输出到输出框
    let a = document.getElementById("abstract");
    a.value = report["abstract"];
    
    let v = document.getElementById("report");
    v.value = report["report"];

}

function reset_button(){
    let i = document.getElementById("in");
    i.value = ""

    let a = document.getElementById("abstract");
    a.value = "";
    
    let v = document.getElementById("report");
    v.value = "";
}

function copy_by_id(id){
    document.getElementById(id).select();
    document.execCommand("Copy"); // 执行浏览器复制命令
    // alert("已复制");
}

function copy_ab(id){
    copy_by_id(id)
    x = document.getElementById("copy_ab")
    temp = x.innerHTML;
    x.innerHTML = "已复制";
    x.disabled=true;
    setTimeout(function (){
        x.disabled=false;
        x.innerHTML = temp;
    },1500);
}
function copy_rp(id){
    copy_by_id(id)
    x = document.getElementById("copy_rp")
    temp = x.innerHTML;
    x.innerHTML = "已复制";
    x.disabled=true;
    setTimeout(function (){
        x.disabled=false;
        x.innerHTML = temp;
    },1500);
}