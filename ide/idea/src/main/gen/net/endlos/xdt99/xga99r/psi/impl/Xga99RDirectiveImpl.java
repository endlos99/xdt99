// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99r.psi.Xga99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99r.psi.*;

public class Xga99RDirectiveImpl extends ASTWrapperPsiElement implements Xga99RDirective {

  public Xga99RDirectiveImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99RVisitor visitor) {
    visitor.visitDirective(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99RVisitor) accept((Xga99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xga99RArgsDirC getArgsDirC() {
    return findChildByClass(Xga99RArgsDirC.class);
  }

  @Override
  @Nullable
  public Xga99RArgsDirF getArgsDirF() {
    return findChildByClass(Xga99RArgsDirF.class);
  }

  @Override
  @Nullable
  public Xga99RArgsDirN getArgsDirN() {
    return findChildByClass(Xga99RArgsDirN.class);
  }

  @Override
  @Nullable
  public Xga99RArgsDirS getArgsDirS() {
    return findChildByClass(Xga99RArgsDirS.class);
  }

  @Override
  @Nullable
  public Xga99RArgsDirT getArgsDirT() {
    return findChildByClass(Xga99RArgsDirT.class);
  }

}
