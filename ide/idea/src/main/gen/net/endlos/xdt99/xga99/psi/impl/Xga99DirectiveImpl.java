// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99.psi.Xga99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99.psi.*;

public class Xga99DirectiveImpl extends ASTWrapperPsiElement implements Xga99Directive {

  public Xga99DirectiveImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99Visitor visitor) {
    visitor.visitDirective(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99Visitor) accept((Xga99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xga99ArgsDirC getArgsDirC() {
    return findChildByClass(Xga99ArgsDirC.class);
  }

  @Override
  @Nullable
  public Xga99ArgsDirF getArgsDirF() {
    return findChildByClass(Xga99ArgsDirF.class);
  }

  @Override
  @Nullable
  public Xga99ArgsDirN getArgsDirN() {
    return findChildByClass(Xga99ArgsDirN.class);
  }

  @Override
  @Nullable
  public Xga99ArgsDirS getArgsDirS() {
    return findChildByClass(Xga99ArgsDirS.class);
  }

  @Override
  @Nullable
  public Xga99ArgsDirT getArgsDirT() {
    return findChildByClass(Xga99ArgsDirT.class);
  }

}
