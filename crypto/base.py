def node_b64(s):
	i=0;base64=ending='';base64chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';pad=3-len(s)%3
	if pad!=3:s+='A'*pad;ending+='='*pad
	while i<len(s):
		b=0
		for j in range(0,3,1):n=ord(s[i]);i+=1;b+=n<<8*(2-j)
		base64+=base64chars[b>>18&63];base64+=base64chars[b>>12&63];base64+=base64chars[b>>6&63];base64+=base64chars[b&63]
	if pad!=3:base64=base64[:-pad];base64+=ending
	return base64