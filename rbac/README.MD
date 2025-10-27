RBAC Setup for EKS Cluster (Step by Step)
1️⃣ IAM User Creation (rbac user)

AWS Console → IAM → Users → Add user

User name: rbac

Access type: Programmatic access

Attach policy: AmazonEKSClusterPolicy


2️⃣ AWS CLI Profile Configuration
aws configure --profile rbac


Input:

AWS Access Key ID: <rbac user's access key>
AWS Secret Access Key: <rbac user's secret key>
Default region name:


Verify:

aws configure list --profile rbac
aws sts get-caller-identity --profile rbac

3️⃣ Map IAM user to Kubernetes RBAC
Edit aws-auth ConfigMap
kubectl edit configmap aws-auth -n kube-system


Replace or add mapUsers section:

apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::961341553264:role/project_eks_node_group_role
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
  mapUsers: |
    - userarn: arn:aws:iam::961341553264:user/rbac
      username: rbac
      groups:
        - system:masters


Important:

userarn absulately real IAM user ARN 

Save & exit। Wait 10–20 seconds for propagation.


4️⃣ Update kubeconfig using rbac user
aws eks update-kubeconfig --name project --region us-east-1 --profile rbac


Successful show add

5️⃣ Verify Cluster Access
kubectl get nodes
kubectl get pods --all-namespaces


Check RBAC permissions:

kubectl auth can-i get pods --as rbac
kubectl auth can-i create pods --as rbac
kubectl auth can-i delete pods --as rbac


add rbac role 

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: demo-namespace   
  name: pod-reader
rules:
  - apiGroups: [""]          
    resources: ["pods"]       
    verbs: ["get", "list", "watch"]  



add rbac role buinding

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rbac-pod-reader-binding
  namespace: demo-namespace   
subjects:
  - kind: User
    name: rbac               
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader          
  apiGroup: rbac.authorization.k8s.io


# for find certificate-authority-data
aws eks describe-cluster --name clustername --query "cluster.certificateAuthority.data" --output text


