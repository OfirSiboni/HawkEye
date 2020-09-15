#echo "$(sed '/export $1/d' ~/.bashrc)" > ~/.bashrc
sed -i '/export '${1}'/d' ~/.bashrc
echo "export $1=$2" >> ./.bashrc
. ~/.bashrc
exec bash
echo "var $1 value $2"