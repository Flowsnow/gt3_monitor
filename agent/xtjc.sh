#!/bin/bash
#date:2017-05-25
#结果log日志存放tmp目录,文件名必须为x.x.x.x 必须为本机ip,例如logfile=192.168.30.1.log
logfile=/tmp/x.x.x.x.log
#是否为数据库标记,0表示不是数据库服务器,不收集数据库alter日志信息;默认为flag=0,1表示是数据库服务器
flag=0
#是否收集ogg信息，0表示不是ogg服务器，不收集ogg信息;默认为glag=0,1表示是ogg服务器
glag=0
#oracle alert日志文件,例如ORACLE_ALERT=/u01/app/oracle/diag/rdbms/nxltgshx04/nxltgshx04/trace/alert_nxltgshx04.log
ORACLE_ALERT=
#OGG gsgg目录,并请将gginfo.sh放置gsgg目中,例如GG_DIR=/goldengate
GG_DIR=

#服务端服务器主机用户,默认是oracle。使用预生产数据库主机作为服务端服务器，确保该主机可以和所有被检查主机ssh互信。
user=oracle

#服务端服务器主机IP地址,使用预生产数据库主机作为服务端服务器，确保该主机可以和所有被检查主机ssh互信。
ip=x.x.x.x
osbb=`uname -a |awk '{print $1}'`

function cpujc(){
	echo "[cpujc]" > $logfile
	w |head -1 |awk -F 'age:' '{print $2}' |awk '{print "load1="$1"\n", "load5="$2"\n", "load15="$3}' |sed 's/,//g'|sed 's/^[ \t]*//g' >> $logfile
	sar -u 1 5 |tail -1 |awk '{print "user="$3"\n", "kern="$5"\n", "wait="$6"\n", "idle="$8}'|sed 's/^[ \t]*//g' >> $logfile
	echo "" >> $logfile
}

function aixcpujc(){
        echo "[cpujc]" > $logfile
        w |head -1 |awk -F 'age:' '{print $2}' |awk '{print "load1="$1"\n", "load5="$2"\n", "load15="$3}' |sed 's/,//g'|sed 's/^[ \t]*//g' >> $logfile
	vmstat 1 3|tail -1 |awk '{print "user="$13"\n""kern="$14"\n", "wait="$16"\n", "idle="$15}'|sed 's/^[ \t]*//g' >> $logfile
        echo "" >> $logfile
}

function freejc(){
	echo "[freejc]" >> $logfile
	free -m |grep Mem |awk '{print "free="$4"\n", "used="$3"\n", "buff="$6"\n", "cache="$7"\n", "total="$2"\n", "lyl="($3/$2)*100}' |sed 's/^[ \t]//g' >> $logfile
	free -m |grep Swap|awk '{print "stoal="$2"\n", "sused="$3"\n", "sfree="$4}' |sed 's/^[ \t]//g' >> $logfile
	echo "" >> $logfile
}

function aixfreejc(){
        echo "[freejc]" >> $logfile
	svmon -G |grep "memory" |awk '{print "free="$4/1024"\n", "userd="$3/1024"\n", "buff="($2-$1)/1024"\n", "cache=-1\n", "total="$2/1024"\n", "lyl="$3/$2*100}'|sed 's/^[ \t]//g' >> $logfile
	lsps -s |tail -1 |awk '{print "stoal="$1"\n", "suserd="$1*$2/100"\n", "sfree="$1-($1*$2/100)}'|sed 's/^[ \t]//g' >> $logfile
        echo "" >> $logfile
}

function sardjc(){
	echo "[sardjc]" >> $logfile
		sar -d 1 5 |egrep "平均时间|Average" |grep -v DEV |awk '{print $2".util="$10"\n", $2".tps="$3"\n", $2".rdsec="$4"\n", $2".wrsec="$5}' |sed 's/^[ \t]//g' >> $logfile 
	echo "" >> $logfile
}

function aixsardjc(){
        echo "[sardjc]" >> $logfile
	iostat |sed -n "/Disks/,//p" |grep -v "Disks" |awk '{print $1".util="$2"\n", $1".tps="$4"\n", $1".rdsec="$5"\n", $1".wrsec="$6""}' |sed 's/^[ \t]//g' >> $logfile
        echo "" >> $logfile
}

function dfhpjc(){
	echo "[dfhpjc]" >> $logfile
	df -hP |egrep -v "文件系统|Filesystem" |awk '{print NR, $0}'|awk '{ print "wjxt"$1"="$2"\n", "wjxt"$1".rl="$3"\n", "wjxt"$1".yy="$4"\n", "wjxt"$1".ky="$5"\n", "wjxt"$1".yybfb="$6"\n", "wjxt"$1".gzd="$7""}'|sed 's/^[ \t]//g'|sed 's/%//g' >> $logfile
	echo "" >> $logfile
}

function aixdfhpjc(){
        echo "[dfhpjc]" >> $logfile
	df |egrep -v "Filesystem|文件系统" |awk '{print NR, $0}'|awk '{print "wjxt"$1"="$2"\n", "wjxt"$1".rl="$3/1024"M\n", "wjxt"$1".yy="($3-$4)/1024"M\n", "wjxt"$1".ky="$4/1024"M\n", "wjxt"$1".yybfb="$5"\n", "wjxt"$1".gzd="$8""}'|sed 's/^[ \t]//g'|sed 's/%//g' >> $logfile
        echo "" >> $logfile
}

function alertjc(){
	if [ $flag -eq 1 ];then
		echo "[alertjc]" >> $logfile
		j=0
		for i in `tail -900 $ORACLE_ALERT|grep "ORA-"|sed 's/[ \t]//g'`;do
			let j+=1
			echo "error$j='''$i'''" >>$logfile
		done
	fi
}

function oggjc(){
	if [ $glag -eq 1 ];then
		echo "[oggjc]" >> $logfile
		k=1
		e=null
        cd $GG_DIR
		./ggsci <gginfo.sh |awk '{if("MANAGER" == $1 || "EXTRACT" == $1 || "REPLICAT" == $1) {print $1,$2,$3,$4,$5}}'>goldengate_status.log
		arr=($(cat $GG_DIR/goldengate_status.log))
		echo "jincheng1=${arr[0]}" >>$logfile
		echo "jincheng1.status=${arr[1]}" >>$logfile
		echo "jincheng$k.name=$e" >>$logfile
		echo "jincheng$k.lagtime=$e" >>$logfile
		echo "jincheng$k.sincetime=$e" >>$logfile
		for ((n=2;n<${#arr[@]};n+=5));do
				let k+=1
				echo "jincheng$k=${arr[$n]}" >>$logfile
				echo "jincheng$k.status=${arr[$n+1]}" >>$logfile
				echo "jincheng$k.name=${arr[$n+2]}" >>$logfile
				echo "jincheng$k.lagtime=${arr[$n+3]}" >>$logfile
				echo "jincheng$k.sincetime=${arr[$n+4]}" >>$logfile
			done
	fi
}

if [ $osbb == "Linux" ];then
	cpujc
	freejc
	sardjc
	dfhpjc
	alertjc
	oggjc
	scp $logfile $user@$ip:/home/$user/file
elif [ $osbb == "AIX" ];then
	aixcpujc
	aixfreejc
	aixsardjc
	aixdfhpjc
	alertjc
	oggjc
	scp $logfile $user@$ip:/home/$user/file
fi
