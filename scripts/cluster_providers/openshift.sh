#!/bin/bash -e 

function create_cluster(){
   echo "\nOpenshift cluster provider"
   echo "\nOpenshift requires PV to be set before starting the tests"
   export KUBECONFIG=$1
   cat <<EOF | kubectl apply -f -
         apiVersion: v1
         kind: PersistentVolume
         metadata:
           name: test-pv
         spec:
           capacity:
             storage: 10Gi
           accessModes:
             - ReadWriteOnce
           persistentVolumeReclaimPolicy: Retain
           storageClassName: standard
           nfs:
             path: /tmp
             server: 172.17.0.2
EOF

   echo "Sleep for 10 secs"
   sleep 10
}

function delete_cluster() {
   echo "\nCluster deletion will not be performed on external cluster"
   echo "\nDeleting resources created for the tests"
   export KUBECONFIG=$(get_cluster_auth)
   kubectl delete pv test-pv
}

function get_cluster_auth() {
   echo "export KUBECONFIG=$1"
}
